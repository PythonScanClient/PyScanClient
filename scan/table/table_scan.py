"""
Table Scan Support
==================

Creates a scan based on a table.

Basic Example
-------------

Each column of a table specifies a device name (Process Variable).
Cells in each row provide the desired values.

+-----------+---------+
|temperature|position |
+-----------+---------+
|   50      |   1     |
+-----------+---------+
|  100      |   2     |
+-----------+---------+

The table above creates the following scan commands::

   Set('temperature', 50),
   Set('position', 1),
   Set('temperature', 100),
   Set('position', 2),


Cells can remain empty if a device should not be changed in that row.

+-----------+---------+
|temperature|position |
+-----------+---------+
|   50      |   1     |
+-----------+---------+
|           |   2     |
+-----------+---------+
|           |   3     |
+-----------+---------+
|  100      |   1     |
+-----------+---------+
|           |   2     |
+-----------+---------+
|           |   3     |
+-----------+---------+

Results in::

   Set('temperature', 50),
   Set('position', 1),
   Set('position', 2),
   Set('position', 3),
   Set('temperature', 100),
   Set('position', 1),
   Set('position', 2),
   Set('position', 3),


Ranges, Lists
-------------

Cells that contain a `range()` command or list will be expanded,
resulting in this shorter version of the previous table,
using both 'range(1,4,1)' and '[1, 2, 3]' to create the same sequence of position values:

+-----------+------------+
|temperature|position    |
+-----------+------------+
|   50      |range(1,4,1)|
+-----------+------------+
|  100      |[1, 2, 3]   |
+-----------+------------+

Within a row, multiple ranges or lists are recursively expanded from right to left.
This shorter table results in the same scan commands:

+-----------+------------+
|temperature|position    |
+-----------+------------+
| [50,100]  | [1, 2, 3]  |
+-----------+------------+



Scan Settings
-------------

In addition to simply writing to a device,
the 'Set' command can wait for completion
and compare a readback from either the original device name (Process Variable)
or a different one.

When for example accessing a 'position' device associtated with an EPICS motor,
the 'Set' command should await completion,
then compare the 'position.RBV' against the desired position.
The tolerance for this comparison as well as a timeout will depend on the actual
motor.

The 'ScanSettings' class is used to configure which PVs use completion,
their timeout, the name of an associated readback.

.. literalinclude:: ../example/scan_settings1.py


Code Example
-------------

.. literalinclude:: ../example/table1.py

'Wait For', 'Value' Columns
---------------------------

These special columns result in `Wait` command.

"""
# @author: Kay Kasemir

import scan.commands as cmds
from range_helper import expandRanges

class TableScan:
    """
    Creates scan commands based on a table.
    """
    
    # Predefined columns
    COMMENT = "Comment"
    WAITFOR = "Wait For"
    VALUE = "Value"
    OR_TIME = "Or Time"
    COMPLETION = "completion"
    SECONDS = "seconds"
    
    def __init__(self, settings, headers, rows, pre=None, post=None, start=None, stop=None):
        """
        Initialize Table scan
        
        Parameters:
        settings:     ScanSettings
        headers[]:    Column headers of the table
        rows[][]:     Rows of the scan. Each row must have len(headers) columns.
        pre:          Command or list of commands executed at the start of the table.
                      Could be used to 'arm' data aquisition.
        post:         Command or list of commands executed at the end of the table.
                      Could be used to close data aquisition.
        start:        Command or list of commands executed to start each 'Wait For'.
                      Could be used to reset counters, trigger data acquisition.
        stop:         Command or list of commands executed at the end of each 'Wait For'.
                      Could be used to inform data acquisition that one step of the scan has completed.
        """
        self.settings = settings
        self.name = "Table Scan"
        self.pre = self.__makeList(pre)
        self.post = self.__makeList(post)
        self.start = self.__makeList(start)
        self.stop = self.__makeList(stop)
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
    
    def __makeList(self, cmd):
        if isinstance(cmd, cmds.Command):
            return [ cmd ]
        if cmd:
            return list(cmd)
        return None
    
    def __getValue(self, text):
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
        if self.pre:
            commands += self.pre
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
                    value = self.__getValue(row[i+1])

                    if waitfor.lower() != TableScan.COMPLETION  and  parallel_commands:
                        # Complete accumulated parallel_commands before starting the run
                        commands.append(cmds.Parallel(parallel_commands))
                        parallel_commands = list()

                    # Optional commands to mark start of a "Wait For"
                    if self.start:
                        commands += self.start

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

                    # Optional commands to mark end of a "Wait For"
                    if self.stop:
                        commands += self.stop
                    
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
                    value = self.__getValue(row[i])
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
        
        if self.post:
            # End one long run at end of table
            commands += self.post
        
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
    
