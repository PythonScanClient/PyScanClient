from scan import CommandSequence
from scan.util.seconds import parseSeconds
from scan.commands import Delay
from scan.table import TableScan

# A table column "XYZ" will write its cell values to PV "XYZ".
# Out of the box, a column "Delay" will simply write to a PV "Delay".
print("==== Default behavior of a 'Delay' column")
table = TableScan(
      ['+p temperature', '+p position', 'Delay'],
    [ [      50,           1,            10,   ],
    ])
scan = table.createScan()
print(table)
print(CommandSequence(scan))

# A special column handler can change this.
# In this example, "Delay" cells turn into Delay(seconds) commands
special_columns = dict()
special_columns['Delay'] = lambda cell:  Delay(parseSeconds(cell))

print("==== Table where 'Delay' column turns into a Delay")
table = TableScan(
      ['+p temperature', '+p position', 'Delay'],
    [ [      50,           1,            10,   ],
    ],
    special=special_columns)
print(table)
scan = table.createScan()
print(CommandSequence(scan))
