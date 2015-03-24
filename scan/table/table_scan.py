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
    COMPLETION = "completion"
    SECONDS = "seconds"
    
    def __init__(self, settings, headers, rows, run_per_line=True):
        """
        Initialize Table scan
        
        Parameters:
        settings:     ScanSettings
        headers[]:    Header columns of the table
        rows[][]:     Rows of the scan. Each row must have len(headers) columns.
        run_per_line: True to create one 'run' per line,
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
        # In addition, measure the width of each column
        # and skip empty rows
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
           text: Text that may contain numeric value
           Returns Number or text.
        """ 
        try:
            return float(text)
        except ValueError:
            return text # Keep as string
    
    def createScan(self):
        """Create scan for complete table
           Returns list of commands.
        """
        
        # Parse column headers.
        col_device = [ None for i in range(self.cols) ]
        col_parallel = [ None for i in range(self.cols) ]
        i = 0
        while i < self.cols:
            if self.headers[i] == TableScan.WAITFOR:
                # Column TableScan.WAITFOR must be followed by TableScan.VALUE
                if i >= self.cols-1  or  self.headers[i+1] != TableScan.VALUE:
                    raise ValueError(TableScan.WAITFOR + " column must be followed by " + TableScan.VALUE)
                # .. and may then be followed by TableScan.OR_TIME
                if i < self.cols-2  and  self.headers[i+2] == TableScan.OR_TIME:
                    i += 2
                else:
                    i += 1
            elif self.headers[i] in ( TableScan.COMMENT ):
                # Ignore other special columns
                pass
            else:
                # Parse device info
                (col_device[i], col_parallel[i])  = self.settings.parseDeviceSettings(self.headers[i])
            i += 1
        
        # Expand any range(start, end, step) cells
        expanded_rows = expandRanges(self.rows)
        
        # Assemble commands for each row in the table
        commands = list()
#         log_devices = list(self.settings.log_always)
        log_devices = list()
        if not self.run_per_line:
            # Create one long run, started before first line
            commands.append(Include("start.scn"))
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

                    if waitfor.lower() != TableScan.COMPLETION  and  parallel_commands:
                        # Complete accumulated parallel_commands before starting the run
                        commands.append(cmds.Parallel(parallel_commands))
                        parallel_commands = list()

                    if self.run_per_line:
                        # Start (& stop) for each line
                        commands.append(cmds.Include("start.scn", ""))
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

                    if waitfor.lower() == TableScan.COMPLETION:
                        # Assert that there are any parallel commands,
                        # because otherwise the 'WaitFor - Completion' was likely an error
                        if not parallel_commands:
                            raise Exception("Line %d has no parallel commands to complete" % line)
                        commands.append(cmds.Parallel(parallel_commands))
                        parallel_commands = list()
                    elif waitfor.lower() == TableScan.SECONDS:
                        commands.append(cmds.Delay(value))
                    else:
                        (device, parallel) = self.settings.parseDeviceSettings(waitfor)
                        timeout = device.getTimeout()
                        errhandler = None
                        if i+2 < self.cols  and  self.headers[i+2] == TableScan.OR_TIME:
                            or_time = row[i+2].strip()
                            if len(or_time) > 0:
                                timeout = float(or_time)
                                errhandler = "OnErrorContinue"
                        cmd = cmds.Wait(device.getName(), value, comparison=device.getComparison(),
                                        tolerance=device.getTolerance(), timeout=timeout, errhandler=errhandler)
                        commands.append(cmd)
                        if not device.getName() in log_devices:
                            log_devices.append(device.getName())
                    
                    if len(log_devices) > 0:
                        commands.append(cmds.Log(log_devices))

                    if self.run_per_line:
                        # (Start &) stop for each line
                        commands.append(cmds.Include("stop.scn"))
                    else:
                        # Mark end of scan step
                        if self.settings.mark_scan_steps:
                            cmd = '%s:CS:Scan:Step:Control' % self.settings.S
                            commands.append(SetCommand(cmd, 3, True, cmd, False, 0.1, 20))
                    
                    # Skip TableScan.VALUE in addition to current column,
                    # so next two Exceptions should not happen unless there's an empty "WAIT_FOR"
                    if i+2 < self.cols  and  self.headers[i+2] == TableScan.OR_TIME:
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
                    command = cmds.Set(device.getName(), value,
                                       completion=device.getCompletion(), readback=device.getReadback(),
                                       timeout=device.getTimeout(), tolerance=device.getTolerance())
                        
                    if col_parallel[i]:
                        parallel_commands.append(command)
                    else:
                        commands.append(command)
                    
                    if not device.getName() in log_devices:
                        log_devices.append(device.getName())
                i = i + 1
            # End of columns in row
            # Complete accumulated parallel commands
            if parallel_commands:
                commands.append(cmds.Parallel(parallel_commands))
                parallel_commands = list()
        
        if not self.run_per_line:
            # End one long run at end of table
            commands.append(Include("stop.scn", ""))
        
        return commands

        
    def __repr__(self):
        """Returns table as columnized string."""
        result = 'headers=[ "'
        line = []
        for c in range(self.cols):
            line.append(self.headers[c].ljust(self.width[c]))
        result += '", "'.join(line)
        result += '" ]\nrows= ['
        for row in self.rows:
            line = []
            for c in range(self.cols):
                line.append(row[c].ljust(self.width[c]))
            result += ' [ "' + '", "'.join(line) + '" ],\n       '
        result += "]"
        return result
    
