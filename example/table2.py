from scan_settings1 import MyScanSettings
from scan.table import TableScan

# Custom settings configure the TableScan to
# check 'temperature' for completion,
# and to treat 'position' as a motor with readback check via *.RBV 
settings = MyScanSettings()

# Table scan with these settings,
# definition of column headers,
# and rows
table = TableScan(settings,
      ['position', 'Wait For', 'Value'],
    [ [      2,    'counter',   10000 ],
      [      4,    'seconds',      20 ],
    ])

# Create scan, print each command
scan = table.createScan()
for cmd in scan:
    print cmd
"""
Result:

Set('position', 2.0, completion=true, readback='position.RBV', timeOut=100)
Wait('counter', 10000.0, comparison='>=')
Log('position', 'counter')
Set('position', 4.0, completion=true, readback='position.RBV', timeOut=100)
Delay(20)
Log('position', 'counter')
"""


table = TableScan(settings,
      ['+p x', '+p y', 'Wait For', 'Value'  ],
    [ [     1,      2, 'counter',  10000 ],
      [     3,      4, 'completion', '' ],
    ])

# Create scan, print each command
scan = table.createScan()
for cmd in scan:
    print cmd
"""
Result:
"""
