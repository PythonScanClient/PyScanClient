"""
Table Scan
==========

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

   Comment('# Line 1'),
   Set('temperature', 50),
   Set('position', 1),
   Comment('# Line 2'),
   Set('temperature', 100),
   Set('position', 2),
   Comment('# End'),


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


Loops
-----

Cells can contain `loop(start, end, step)` to set a device in a loop:

+-------------+
|position     |
+-------------+
|loop(2, 5, 1)|
+-------------+

Results in this loop to set the 'position' to 2, 3, 4 and then 5::

   Loop('position', 2, 5, 1)

When using `loop(start, end)` without specifying `step`, the step defaults to 1.

Colummns following a `loop` are handled inside the loop:

+-------------+--------+
|position     | camera |
+-------------+--------+
|loop(2, 5, 1)| snap   |
+-------------+--------+

Results in a loop for the position, triggering a camera at each position::

   Loop('position', 0, 3, 0.5,
        [ Set('camera', 'snap') ]
       )

Loops can be nested, again placing columns following a `loop` inside that loop:

+-----------+-----------+--------+
|X          | Y         | camera |
+-----------+-----------+--------+
|loop(1, 10)| loop(2, 5)|snap    |
+-----------+-----------+--------+

Results in an outer loop for the X position with an inner loop for the Y position, triggering a camera at each position::

   Loop('X', 1, 10, 1,
        [ Loop('Y', 2, 5, 1,
               [ Set('Camera', 'Snap') ]
              )
        ]
       )

When using nested loops, note details regarding 
:ref:`Loop Direction <loop-direction>`
which can be used for reversing the direction of inner loops
to more efficiently scan a surface.


Lists, Ranges
-------------

Cells that contain a list of values or a `range()` command will be expanded
as if you had entered separate rows for each value:

+-------------+
|position     |
+-------------+
|[1, -3, 7, 2]|
+-------------+

is equivalent to

+---------+
|position |
+---------+
| 1       |
+---------+
| -3      |
+---------+
| 7       |
+---------+
| 2       |
+---------+

Compared to a `loop` which always generates equidistant values,
the list can contain any sequence of values.

The `range` behaves similar to the Python `range(start, stop, step)` command,
generating values from `start` up to but **excluding** `stop`.

+------------+
|position    |
+------------+
|range(1,4,1)|
+------------+

is equivalent to

+---------+
|position |
+---------+
| 1       |
+---------+
| 2       |
+---------+
| 3       |
+---------+

`loop(start, end, step)` should be preferred over `range(start, stop, step)`
because of the inclusive and thus more obvious handling of `end` vs. `stop`.

In addition, each `loop` translates into a single `Loop` command:

+----------------+
|position        |
+----------------+
|loop(1,100,0.1) |
+----------------+

becomes::

   Loop('position', 1, 100, 0.1)

This `range`-based table will set `position` to the same values:

+-------------------+
|position           |
+-------------------+
|range(1,100.1,0.1) |
+-------------------+

The resulting scan, however, becomes a sequence of 1000 `Set` commands::

   Set('position', 1)
   Set('position', 1.1)
   Set('position', 1.2)
   ...
   Set('position', 99.9)
   Set('position', 100)

For larger loops respectively ranges, the loop will be more efficient.

Within a row, multiple ranges or lists are recursively expanded from right to left,
similar to the nesting of loops:

+-----------+------------+
|temperature|position    |
+-----------+------------+
| [50,100]  | [1, 2, 3]  |
+-----------+------------+

is expanded into

+-----------+------------+
|temperature|position    |
+-----------+------------+
|  50       |  1         |
+-----------+------------+
|  50       |  2         |
+-----------+------------+
|  50       |  3         |
+-----------+------------+
| 100       |  1         |
+-----------+------------+
| 100       |  2         |
+-----------+------------+
| 100       |  3         |
+-----------+------------+


Scan Settings
-------------

When for example accessing a 'position' device associtated with an EPICS motor,
the `Set` command should await completion,
then compare the 'position.RBV' against the desired position::

   Set('position', 2, completion=True, readback='position.RBV', tolerance=0.1)

The tolerance for this comparison as well as a timeout will depend on the actual
motor.

You may have a known list of device names and how they need to be accessed,
or you may be able to derive this information based on a naming standard for devices
at your site.

The :mod:`scan.util.scan_settings` module is used to configure how the
`TableScan` accesses devices.


Code Example
-------------

.. literalinclude:: ../example/table1.py

'Wait For', 'Value', 'Or Time' Columns
--------------------------------------

These two columns create commands that wait for
a condition, and then log all devices which
have been used within the scan up to that point.

If the cell contains a device name,
a `Wait` command is created for the device to reach the given value.

+----------+------------+--------+
|position  |Wait For    |  Value |
+----------+------------+--------+
|  2       | counter    | 10000  |
+----------+------------+--------+

The table above will create the following scan::

    Set('position', 2.0, completion=true, readback='position.RBV', timeout=100)
    Wait('counter', 10000.0, comparison='>=')
    Log('position', 'counter')

The :class:`~scan.util.scan_settings.ScanSettings` 
determine the detailed options of the `Set` and `Wait` commands.
By default, the generated `Wait` command will wait forever,
unless the `ScanSettings` provide a timeout.
In the example above, we assume that the `ScanSetting` cause every access
to the 'position' device to use completion and readback.

A prefix `-c` can disable the completion check:

+--------------+------------+--------+
|-c position   |Wait For    |  Value |
+--------------+------------+--------+
|  2           | counter    | 10000  |
+--------------+------------+--------+

Resulting scan without completion for the 'position'::

    Set('position', 2.0, readback='position.RBV', timeout=100)
    Wait('counter', 10000.0, comparison='>=')
    Log('position', 'counter')

For more prefix options see :class:`~scan.util.scan_settings.ScanSettings`.


Waiting for `seconds` or `time` results in a simple `Delay`.

+----------+------------+--------+
|position  |Wait For    |  Value |
+----------+------------+--------+
|  2       | seconds    |   20   |
+----------+------------+--------+
|  4       | time       |   20   |
+----------+------------+--------+

The table above will create the following scan::

    Set('position', 2.0, completion=true, readback='position.RBV', timeout=100)
    Delay(20)
    Log('position')
    Set('position', 4.0, completion=true, readback='position.RBV', timeout=100)
    Delay(20)
    Log('position')

The delay is specified in seconds, a "HH:MM:SS" notation for hours, minutes, seconds,
or "MM:SS" for minutes, seconds.
When using "HH:MM:SS" or "MM:SS", `time` may be a more appropriate 'Wait For' condition,
but either `seconds` or `time` are permitted.
The following rows are all equivalent:

+----------+------------+----------+
|position  |Wait For    |  Value   |
+----------+------------+----------+
|  1       | seconds    |      120 |
+----------+------------+----------+
|  1       | time       |    01:00 |
+----------+------------+----------+
|  1       | seconds    | 00:01:00 |
+----------+------------+----------+
|  1       | time       | 00:01:00 |
+----------+------------+----------+


A column 'Or Time' can be added to allow the scan to continue even if the condition is **not** met:

+----------+------------+--------+----------+
|position  |Wait For    |  Value | Or Time  |
+----------+------------+--------+----------+
|  [2,4,7] | counter    | 10000  | 01:00:00 |
+----------+------------+--------+----------+

The scan generated by this table will set the 'position' to three different values.
At each step, it will wait until either the 'counter' reaches a value of 10000,
or one hour passes.


Parallel Commands
-----------------

Device columns are typically processed sequentially from left to right,
but sometimes it can be useful to for example command two motors or
temperature controllers in parallel, waiting for both to proceed at the
same time, waiting until both of them reach their respective desired value.

Device columns with a `+p` prefix are accessed in parallel.
In this table, devices A and B will be commanded to some value,
waiting for both to get there in parallel.
Next, device C is set to some value.
Once it reaches its value, devices D and E are again commanded in parallel,
and finally device F is set to a value.

+------+------+---+------+------+---+
| +p A | +p B | C | +p D | +p E | F |
+------+------+---+------+------+---+
|  1   |  2   | 3 |  4   | 5    | 6 |
+------+------+---+------+------+---+

Result::

    Parallel(Set('A', 1.0), Set('B', 2.0))
    Set('C', 3.0)
    Parallel(Set('D', 4.0), Set('E', 5.0))
    Set('F', 6.0)

Columns that set devices in parallel need to be adjacent.
Whenever the next column does **not** use `+p`, the previously accumulated
parallel commands are executed.

If the next column is 'Wait For', the behavior depends on the 'Wait For' condition.
If the special condition `completion` is used, the `Wait For` will perform the
accumulated parallel commands.
For other conditions, the accumulated commands are executed and then the 
`Wait For` awaits the requested condition as usual.
In this example we also assume that `Wait For` uses start/stop commands
as explained below.

+------+------+---+------+------+------------+--------+
| +p A | +p B | C | +p D | +p E | Wait For   |  Value |
+------+------+---+------+------+------------+--------+
|  1   |  2   | 3 |  4   |  5   | completion |        |
+------+------+---+------+------+------------+--------+
|  6   |  7   | 8 |  9   | 10   | Seconds    |  10    |
+------+------+---+------+------+------------+--------+

Result::

    Parallel(Set('A', 1.0), Set('B', 2.0))
    Set('C', 3.0)
    Comment('Start Run')
    Parallel(Set('D', 4.0), Set('E', 5.0))
    Log('A', 'B', 'C', 'D', 'E')
    Comment('Stop Run')
    Parallel(Set('A', 6.0), Set('B', 7.0))
    Set('C', 8.0)
    Parallel(Set('D', 9.0), Set('E', 10.0))
    Comment('Start Run')
    Delay(10)
    Log('A', 'B', 'C', 'D', 'E')
    Comment('Stop Run')


Note that the 'Wait For' with `completion` can be useful even for a single parallel command.
In this example, A is written by itself, not in parallel with other operations,
but the parallel mechanism allows you to wait for the completion, i.e.
a run is started and then stopped while A is set:

+------+------------+--------+
| +p A | Wait For   |  Value |
+------+------------+--------+
|  1   | completion |        |
+------+------------+--------+


Result::

    Comment('Start Run')
    Parallel(Set('A', 1.0))
    Log('A')
    Comment('Stop Run')
    




Another example, which again includes start/stop commands
as well as a special `Delay` column as described below:

+------+------+----------+------------+--------+
| +p A | +p B | Delay    | Wait For   |  Value |
+------+------+----------+------------+--------+
|  1   |  2   | 00:05:00 |  counts    |  10    |
+------+------+----------+------------+--------+

Result::

    Parallel(Set('A', 1.0), Set('B', 2.0))
    Delay(300)
    Comment('Start Run')
    Wait('counts', 10.0, comparison='>=', tolerance=0.1)
    Log('A', 'B', 'counts')
    Comment('Stop Run')



Log Additional Devices
----------------------

The example just shown ends in::
   
    Log('x', 'y', 'counter')

because all devices used in a row are logged upon completing the 'Wait For' condition.
These devices could have been affected by a column that set them to a value,
or the 'Wait For' condition depended on the device.

To log additional devices, even though they are otherwise not mentioned in the table,
pass the `log_always` parameter to the table::

    table = TableScan(headers, rows, log_always=[ 'neutrons' ])
    
will include the device `neutrons` whenever it logs values at the end of a row.


Pre, Post, Start and Stop Commands
----------------------------------

Both the devices listed in the table column headers
and the values used in the cells of the rows of the
table are typically edited for different runs of
an experiment.

There are, however, often the same actions that need
to happen before and after the complete table is executed,
as well as at each step of a table.

You can provide a list of commands for the following steps:

`pre`:
    Before executing the table rows.
    Example: Open a beam line shutter.

`post`:
    After executing all table rows.
    Example: Close a beam line shutter.

`start`:
    Before each 'Wait For'.
    Example: Zero counter PVs, in fact counters 
    which the 'Wait For' command will then check
    to reach a certain value, and start data acquisition.

`stop`:
    After each 'Wait For' completes.
    Example: Stop data acquisition.


Special Column handling
-----------------------

Going back to the most basic behavior of the table scan,
given a column name and a cell value, each non-empty cell
results in a command::

   Set(column_name, cell_value)

For example, a column named "RunControl" with cell values "start" and "stop":

+------------+
| RunControl |
+------------+
| Start      |
+------------+
| Stop       |
+------------+

would result in these commands::

   Set("RunControl", "Start")
   Set("RunControl", "Stop")

Assuming that the process variable "RunControl" is an enumerated type with valid states "start" and "stop",
maybe connected to an IOC sequence to start and stop a data acquisition run, this will work just fine.

Extending the example, assume that you would rather use "Run Control" as a column name to distinguish it from
an ordinary process variable, and the cell values should result in `Include` commands.

Another example would be a "Delay" column that should turn into a plain delay.

To handle such special cases, the `TableScan` API allows you to provide a dictionary with special column handler functions.
Each function is called with the value of the cell, and it must return a scan command.

Example::

    from scan.util.seconds import parseSeconds
    special_handlers = { 'Run Control': lambda cell : Include(cell + ".scn"),
                         'Delay':       lambda cell : Delay(parseSeconds(cell)),
                       }
    table_scan = TableScan(
      (   "Run Control", "X",  "Delay",    "Wait For", "Value", ),
      [
        [ "Start",       "10", "",         "Neutrons", "10" ],
        [ "",            "20", "00:01:00", "Neutrons", "10" ],
        [ "Stop",        "",   "",         "",         "" ],
      ],
      special = special
    )

When handling cells for the "Run Control" column, the special handler function
will now be invoked with the cell values, i.e. "Start" and "Stop"::
   
    lambda cell : Include(cell + ".scn")

resulting in these commands::

    Include("Start.scn")
    Include("Stop.scn")

The "Delay" column will invoke this handler::
    
    lambda cell : Delay(parseSeconds(cell))

resulting in this for the above example::

    Delay(60)

The special handler function can wrap multiple commands as a :class:`~scan.commands.sequence.Sequence` command.


API
---
"""
# @author: Kay Kasemir

from scan.commands import Command, Comment, Delay, Log, Parallel
from scan.util.scan_settings import getScanSettings, SettingsBasedSet, SettingsBasedLoop, SettingsBasedWait
from scan.util.seconds import parseSeconds
from range_helper import getRangeOrLoop, loop_matcher, expandRanges
from scan.util.spreadsheet import readSpreadsheet, writeSpreadsheet

def loadTableScan(filename, pre=None, post=None, start=None, stop=None):
    """Load table from spreadsheet file
       
    :param filename:     File name, either '*.cvs', '*.tab', '*.xls' or '*.gnumeric'
    :param pre:          Command or list of commands executed at the start of the table.
    :param post:         Command or list of commands executed at the end of the table.
    :param start:        Command or list of commands executed to start each 'Wait For'.
    :param stop:         Command or list of commands executed at the end of each 'Wait For'.
    """
    table = readSpreadsheet(filename)
    headers = table[0]
    rows = table[1:]
    return TableScan(headers, rows, pre, post, start, stop)

class TableScan:
    """Create Table scan
    
    :param headers[]:    Column headers of the table
    :param rows[][]:     Rows of the scan. Each row must have len(headers) columns.
    :param pre:          Command or list of commands executed at the start of the table.
    :param post:         Command or list of commands executed at the end of the table.
    :param start:        Command or list of commands executed to start each 'Wait For'.
    :param stop:         Command or list of commands executed at the end of each 'Wait For'.
    :param log_always:   Optional list of device names that should be logged in addition
                         to those that are affected by columns that set them
                         or 'Wait For' conditions.
    :param special:      Dictionary with special column handlers
    """
    
    # Predefined columns
    COMMENT = "Comment"
    WAITFOR = "Wait For"
    VALUE = "Value"
    OR_TIME = "Or Time"
    COMPLETION = "completion"
    SECONDS = "seconds"
    TIME = "time"
    
    def __init__(self, headers, rows, pre=None, post=None, start=None, stop=None, log_always=None, special=dict()):
        self.name = "Table Scan"
        self.pre = self.__makeList(pre)
        self.post = self.__makeList(post)
        self.start = self.__makeList(start)
        self.stop = self.__makeList(stop)
        self.special = special
        self.log_always=log_always
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

        if not (isinstance(rows, list)
                and 
                all(isinstance(row, list) for row in rows)):
            raise ValueError("Table needs list of rows, but got %s" % str(rows))

        for r in range(len(rows)):
            row = rows[r]
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
                raise ValueError("Table has %d columns but row %d has only %d" % (len(self.headers), r, len(patched_row)))
            if not is_empty:
                self.rows.append(patched_row)
    
    def save(self, filename):
        """Save table to file
    
        Writes table as CSV file.
    
        :param filename: File path, must end in ".csv" or ".tab"
        """
        table = [ self.headers ] + self.rows
        writeSpreadsheet(filename, table)

    def __makeList(self, cmd):
        if isinstance(cmd, Command):
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
    
    def __flushParallel(self, commands):
        """:param commands: Where accumulated parallel commands are appended
           :return: True if there were any parallel commands
        """
        if len(self.parallel_commands) > 0:
            # Complete accumulated parallel_commands before starting the run
            commands.append(Parallel(self.parallel_commands))
            self.parallel_commands = list()
            return True
        return False
    
    def createScan(self, lineinfo=True):
        """Create scan.

        :param lineinfo: By default Comment commands are added for line info.
                         If scan settings include a "table_scan_row",
                         that PV will also be set.
        :return: List of commands.
        """
        # Parse column headers.
        settings = getScanSettings()
        col_device = [ None for i in range(self.cols) ]
        i = 0
        while i < self.cols:
            if self.headers[i].lower() == TableScan.WAITFOR.lower():
                # Column TableScan.WAITFOR must be followed by TableScan.VALUE
                if i >= self.cols-1  or  self.headers[i+1].lower() != TableScan.VALUE.lower():
                    raise ValueError(TableScan.WAITFOR + " column must be followed by " + TableScan.VALUE)
                # .. and may then be followed by TableScan.OR_TIME
                if i < self.cols-2  and  self.headers[i+2].lower() == TableScan.OR_TIME.lower():
                    i += 2
                else:
                    i += 1
            elif self.headers[i].lower() == TableScan.COMMENT.lower():
                # Comment is no device name
                pass
            else:
                # Parse device info
                col_device[i] = settings.parseDeviceSettings(self.headers[i])
            i += 1
        
        # Add first column of line numbers
        numbered = []
        for row in self.rows:
            numbered_row = list(row)
            numbered_row.insert(0, len(numbered)+1)
            numbered.append(numbered_row)
        # Expand any range(start, end, step) cells
        # (which will duplicate the line numbers)
        expanded_rows = expandRanges(numbered)
        
        # Assemble commands for each row in the table
        current_line = 0
        commands = list()
        log_devices = list()
        if self.log_always is not None:
            log_devices = list(self.log_always)
        if self.pre:
            commands += self.pre
        for numbered_row in expanded_rows:
            line = numbered_row[0]
            row = numbered_row[1:]
            row_commands = commands
            if line != current_line:
                if lineinfo:
                    row_commands.append(Comment("# Line %d" % line))
                    if settings.table_scan_row:
                        row_commands.append(SettingsBasedSet(settings.table_scan_row, line))
                current_line = line
            # Parallel commands to execute in this row
            self.parallel_commands = list()
            # Handle all columns
            c = 0
            while c < self.cols:
                what = self.headers[c]
                if len(row[c]) <= 0:
                    pass # Empty column, nothing to do
                elif what in self.special:
                    self.__flushParallel(row_commands)
                    special_handler = self.special[what]
                    value = self.__getValue(row[c])
                    command = special_handler(value)
                    row_commands.append(command)
                elif what.lower() == TableScan.COMMENT.lower():
                    self.__flushParallel(row_commands)
                    text = row[c]
                    row_commands.append(Comment(text))           
                    # TODO if self.settings.comment:
                    #       row_commands.append(SetCommand(self.settings.comment, text))
                elif what.lower() == TableScan.WAITFOR.lower():
                    waitfor = row[c]
                    value = self.__getValue(row[c+1])
                    timeout = 0
                    errhandler = None
                    if c+2 < self.cols  and  self.headers[c+2] == TableScan.OR_TIME:
                        or_time = row[c+2].strip()
                        if len(or_time) > 0:
                            timeout = parseSeconds(or_time)
                            errhandler = "OnErrorContinue"
 
                    if waitfor.lower() != TableScan.COMPLETION:
                        # Complete accumulated parallel_commands before starting the run
                        self.__flushParallel(row_commands)

                    # Optional commands to mark start of a "Wait For"
                    if self.start:
                        row_commands += self.start

                    if waitfor.lower() == TableScan.COMPLETION:
                        # Assert that there are any parallel commands,
                        # because otherwise the 'WaitFor - Completion' was likely an error
                        if self.__flushParallel(row_commands):
                            command = row_commands[-1]
                            if timeout > 0:
                                row_commands[-1] = Parallel(command.getBody(), timeout = timeout, errhandler = errhandler)
                        else:
                            raise Exception("Line %d has no parallel commands to complete" % line)
                    elif waitfor.lower() in ( TableScan.SECONDS, TableScan.TIME ):
                        if value:
                            row_commands.append(Delay(parseSeconds(value)))
                    else:
                        cmd = SettingsBasedWait(waitfor, value, timeout=timeout, errhandler=errhandler)
                        row_commands.append(cmd)
                        waitfor_device = settings.getDefaultSettings(waitfor).getName()
                        if not waitfor_device in log_devices:
                            log_devices.append(waitfor_device)
                    
                    if len(log_devices) > 0:
                        row_commands.append(Log(log_devices))

                    # Optional commands to mark end of a "Wait For"
                    if self.stop:
                        row_commands += self.stop
                    
                    # Skip TableScan.VALUE in addition to current column,
                    # so next two Exceptions should not happen unless there's an empty "WAIT_FOR"
                    if c+2 < self.cols  and  self.headers[c+2].lower() == TableScan.OR_TIME.lower():
                        c = c + 2
                    else:
                        c = c + 1
                elif what.lower() == TableScan.VALUE.lower():
                    raise Exception("Line %d: Found value '%s' in '%s' column after empty '%s' column.\nRow: %s" %
                                    (line, row[c], TableScan.VALUE, TableScan.WAITFOR, str(row)))
                elif what.lower() == TableScan.OR_TIME.lower():
                    raise Exception("Line %d: Found value '%s' in '%s' column after empty '%s' column.\nRow: %s" %
                                    (line, row[c], TableScan.OR_TIME, TableScan.WAITFOR, str(row)))
                else:
                    # 'Normal' column that sets a device directly or in loop
                    device = col_device[c]
                    value = self.__getValue(row[c])
                    
                    if type(value) is float:
                        loop = None
                    else:
                        loop = getRangeOrLoop(str(value), loop_matcher)

                    if loop is None:
                        command = SettingsBasedSet(what, value)
                        if device.getParallel():
                            # Add one more parallel command
                            self.parallel_commands.append(command)
                        else:
                            # Normal command, flush accumulated parallel commands
                            self.__flushParallel(row_commands)
                            row_commands.append(command)
                    else:
                        # Create loop
                        body = list()
                        command = SettingsBasedLoop(what, loop[0], loop[1], loop[2], body)
                        if device.getParallel():
                            self.parallel_commands.append(command)
                        else:                            
                            self.__flushParallel(row_commands)
                            row_commands.append(command)
                            
                            # Place remaining commands in row into body of this loop
                            row_commands = command.getBody()
                    
                    if not device.getName() in log_devices:
                        log_devices.append(device.getName())
                c = c + 1
            # End of columns in row
            # Complete accumulated parallel commands
            self.__flushParallel(row_commands)
        
        # End of row
        if self.post:
            # End one long run at end of table
            commands += self.post
            
        if lineinfo:
            commands.append(Comment("# End"))
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


if __name__ == "__main__":
    from scan.commands.commandsequence import CommandSequence
    table = TableScan([ "A", "B" ],
                    [
                      [ "1", "" ],
                      [ "2", "[5,6,7]"]
                    ])
    cmds = CommandSequence(table.createScan())
    print(table)
    print(cmds)

    table = TableScan([ "A",             "B" ],
                    [
                      [ "Loop(1, 2, 1)", "loop(5, 7, 1)" ]
                    ])
    cmds = CommandSequence(table.createScan())
    print(table)
    print(cmds)

