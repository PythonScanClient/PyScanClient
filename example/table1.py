from scan_settings1 import MyScanSettings, setScanSettings
from scan.table import TableScan

# Custom settings configure the TableScan to
# check 'temperature' for completion,
# and to treat 'position' as a motor with readback check via *.RBV 
setScanSettings(MyScanSettings())

# Table scan with these settings,
# definition of column headers,
# and rows
table = TableScan(
      ['temperature', 'position'],
    [ [      50,           1],
      [      '',           2],
      [      '',           3],
      [     100,           1],
      [      '',           2],
      [      '',           3],
    ])

# Create scan, print each command
scan = table.createScan()
for cmd in scan:
    print cmd
"""
Result:
Set('temperature', 50.0, completion=True, timeout=300)
Set('position', 1.0, completion=True, readback='position.RBV', timeout=100)
Set('position', 2.0, completion=True, readback='position.RBV', timeout=100)
Set('position', 3.0, completion=True, readback='position.RBV', timeout=100)
Set('temperature', 100.0, completion=True, timeout=300)
Set('position', 1.0, completion=True, readback='position.RBV', timeout=100)
Set('position', 2.0, completion=True, readback='position.RBV', timeout=100)
Set('position', 3.0, completion=True, readback='position.RBV', timeout=100)
"""
