"""
Table Scan Support

@author: Kay Kasemir
"""

import scan.commands as cmds
from range_helper import expandRanges

class TableScan:
    """
    Fields
    ------
    name:      Name of the scan
    headers[]: Header columns of the table
    cols:      Number of columns
    rows[][]:  Rows of the scan
    width[]:   Max width of each column
    """
    # Predefined columns
    COMMENT = "Comment"
    WAITFOR = "Wait For"
    VALUE = "Value"
    OR_TIME = "Or Time"
    
    def __init__(self, settings, headers, rows, run_per_line=True):
        """
        Initialize Table scan     
        @param settings: ScanSettings
        @param headers[]: Header columns of the table
        @param rows[][]: Rows of the scan
        @param run_per_line: True to create one 'run' per line,
                             False to create one long run that resets counters
                             and marks scan steps at each 'Wait'
        """
        self.settings = settings
        self.name = "Table Scan"
        self.run_per_line = run_per_line
        # When called with table widget data,
        # values may be java.lang.String u'text'.
        # Convert to plain 'text'.
        #
        # In addition, skip empty rows
        self.headers = [ str(h).strip() for h in headers ]
        self.cols = len(self.headers)
        self.rows = []
        self.width = [ len(h) for h in self.headers ]
        for row in rows:
            is_empty = True
            patched_row = []
            for c in range(len(row)):
                cell = row[c]
                patched = str(cell).strip()
                patched_row.append(patched)
                width = len(patched)
                if width > self.width[c]:
                    self.width[c] = width
                if width > 0:
                    is_empty = False
            if len(patched_row) != len(self.headers):
                raise ValueError("Not all rows have equal number of columns")
            if not is_empty:
                self.rows.append(patched_row)
    
    def getValue(self, text):
        """Get value from text
           @param text: Text that may contain numeric value
           @return: Number or text
        """ 
        try:
            return float(text)
        except ValueError:
            return text # Keep as string
    
    def createScan(self):
        """Create scan for complete table
           @return: list of scan commands
        """
        
        # Parse column headers
        col_device = dict()
        col_completion = dict()
        col_readback = dict()
        col_timeout = dict()
        col_tolerance = dict()
        col_parallel = dict()
        motors = set()
        i = 0
        while i < self.cols:
            if self.headers[i] == TableScan.WAITFOR:
                # Column TableScan.WAITFOR must be followed by TableScan.VALUE
                if i >= cols-1  or  self.headers[i+1] != TableScan.VALUE:
                    raise ValueError(TableScan.WAITFOR + " column must be followed by " + TableScan.VALUE)
                if i < cols-2  and  self.headers[i+2] == TableScan.OR_TIME:
                    i += 2
                else:
                    i += 1
            elif self.headers[i] in ( TableScan.COMMENT ):
                # Ignore other special columns
                pass
            else:
                # Parse device info
#                 (col_device[i], col_completion[i], col_readback[i],
#                  col_timeout[i], col_tolerance[i], col_parallel[i]) = self.settings.parseDeviceModifiers(self.headers[i])

                (col_device[i], col_completion[i], col_readback[i],
                 col_timeout[i], col_tolerance[i], col_parallel[i]) = (self.headers[i], False, False, 0, 0.1, False)
                
                if ":Mot:" in col_device[i]:
                    motors.add(col_device[i])
            i += 1
        
        # Expand any range(start, end, step) cells
        expanded_rows = expandRanges(self.rows)
        
        # Assemble commands for each row in the table
        commands = list()
#         log_devices = list(self.settings.log_always)
        log_devices = list()
        if not self.run_per_line:
            # Create one long run, started before first line
            commands.append(IncludeCommand("start.scn", ""))
            # Log the scan steps?
            if self.settings.mark_scan_steps:
                log_devices.append('%s:CS:Scan:Step:Index' % self.settings.S)
        line = 0
        for row in expanded_rows:
            line += 1
            # Parallel commands to execute in this row
            parallel_commands = list()
            # Handle all columns
            i = 0
            while i < self.cols:
                what = self.headers[i]
                if len(row[i]) <= 0:
                    pass # Empty column, nothing to do
                elif what == TableScan.COMMENT:
                    text = row[i]
                    commands.append(cmds.Comment(text))           
#                     if self.settings.comment:
#                         commands.append(SetCommand(self.settings.comment, text))
                elif what == TableScan.WAITFOR:
                    waitfor = row[i]
                    value = self.getValue(row[i+1])

                    if waitfor.lower() != self.settings.COMPLETION  and  parallel_commands:
                        # Complete accumulated parallel_commands before starting the run
                        commands.append(ParallelCommand(parallel_commands))
                        parallel_commands = list()

                    if self.run_per_line:
                        # Start (& stop) for each line
                        commands.append(IncludeCommand("start.scn", ""))
                    else:
                        # Reset counters, mark start of new scan step
                        if self.settings.reset_counters:
                            # Initially, only one reset PV was supported,
                            # but now we allow single PV or list of PVs.
                            if type(self.settings.reset_counters) in ( list, tuple ):
                                pvs = self.settings.reset_counters
                            else:
                                pvs = ( self.settings.reset_counters, )
                            for pv in pvs:
                                cmd = SetCommand(pv, 1, True, pv, False, 0.1, 20)
                                cmd.setErrorHandler("OnErrorContinue")
                                commands.append(cmd)
                        if self.settings.mark_scan_steps:
                            cmd = '%s:CS:Scan:Step:Control' % self.settings.S
                            commands.append(SetCommand(cmd, 2, True, cmd, False, 0.1, 20))

                    if waitfor.lower() == self.settings.COMPLETION:
                        # Assert that there are any parallel commands,
                        # because otherwise the 'WaitFor - Completion' was likely an error
                        if not parallel_commands:
                            raise Exception("Line %d has no parallel commands to complete" % line)
                        commands.append(ParallelCommand(parallel_commands))
                        parallel_commands = list()
                    elif waitfor.lower() == self.settings.SECONDS:
                        commands.append(DelayCommand(value))
                    elif waitfor in self.settings.incrementors:
                        cmd = WaitCommand(waitfor, Comparison.INCREASE_BY, value)
                        commands.append(cmd)
                        if not waitfor in log_devices:
                            log_devices.append(waitfor)
                        if i+2 < cols  and  self.headers[i+2] == TableScan.OR_TIME:
                            or_time = row[i+2].strip()
                            if len(or_time) > 0:
                                or_time = float(or_time)
                                cmd.setTimeout(or_time)
                                cmd.setErrorHandler("OnErrorContinue")
                    else:
                        cmd = WaitCommand(waitfor, Comparison.AT_LEAST, value)
                        commands.append(cmd)
                        if not waitfor in log_devices:
                            log_devices.append(waitfor)
                        if i+2 < cols  and  self.headers[i+2] == TableScan.OR_TIME:
                            or_time = row[i+2].strip()
                            if len(or_time) > 0:
                                or_time = float(or_time)
                                cmd.setTimeout(or_time)
                                cmd.setErrorHandler("OnErrorContinue")
                    
                    if len(log_devices) > 0:
                        commands.append(LogCommand(log_devices))

                    if self.run_per_line:
                        # (Start &) stop for each line
                        commands.append(IncludeCommand("stop.scn", ""))
                    else:
                        # Mark end of scan step
                        if self.settings.mark_scan_steps:
                            cmd = '%s:CS:Scan:Step:Control' % self.settings.S
                            commands.append(SetCommand(cmd, 3, True, cmd, False, 0.1, 20))
                    
                    # Skip TableScan.VALUE in addition to current column,
                    # so next two Exceptions should not happen unless there's an empty "WAIT_FOR"
                    if i+2 < cols  and  self.headers[i+2] == TableScan.OR_TIME:
                        i = i + 2
                    else:
                        i = i + 1
                elif what == TableScan.VALUE:
                    raise Exception("Line %d: Found value in '%s' after empty '%s'" % (line, TableScan.VALUE, TableScan.WAITFOR))
                elif what == TableScan.OR_TIME:
                    raise Exception("Line %d: Found value in '%s' after empty '%s'" % (line, TableScan.OR_TIME, TableScan.WAITFOR))
                else:
                    # 'Normal' column that sets a device
                    device = col_device[i]
                    value = self.getValue(row[i])
                    # TODO Add readback as Set command supports it
                    #command = cmds.Set(device, value, completion=col_completion[i], readback=col_readback[i],timeOut=col_timeout[i], tolerance=col_tolerance[i])
                    command = cmds.Set(device, value, completion=col_completion[i], timeOut=col_timeout[i], tolerance=col_tolerance[i])
                        
                    if col_parallel[i]:
                        parallel_commands.append(command)
                    else:
                        commands.append(command)
                    
                    if not device in log_devices:
                        log_devices.append(device)
                i = i + 1
            # End of columns in row
            # Complete accumulated parallel commands
            if parallel_commands:
                commands.append(ParallelCommand(parallel_commands))
                parallel_commands = list()
        
        if not self.run_per_line:
            # End one long run at end of table
            commands.append(IncludeCommand("stop.scn", ""))
        
        # Start by waiting for all motors to be idle
#         for motor in motors:
#             idle = self.settings.getMotorIdlePV(motor)
#             if idle:
#                 commands.insert(0, WaitCommand(idle, Comparison.EQUALS, 1, 0.1, 5.0))

        return commands

        
    def __str__(self):
        line = []
        for c in range(self.cols):
            line.append(self.headers[c].ljust(self.width[c]))
        text = "  ".join(line)
        for row in self.rows:
            line = []
            for c in range(self.cols):
                line.append(row[c].ljust(self.width[c]))
            text = text + "\n" + "  ".join(line)
            
        return text
    
