"""
Initialize Table widget with last scan
@author: Kay Kasemir
"""

from org.csstudio.display.builder.runtime.script import PVUtil
from scan.table.table_scan import TableScan
from tablescan_ui import getTableFromPath, displayTableInWidget

# Try to load table from file
path = PVUtil.getString(pvs[1])
table_scan = None

try:
    table_scan = getTableFromPath(path)
except:
    table_scan = None
    pvs[1].setValue("")

# Create default table if nothing loaded
if not table_scan:
    table_scan = TableScan(
    [ "motor_x", TableScan.WAITFOR, TableScan.VALUE, TableScan.OR_TIME ],
    [
        [ "1",            TableScan.SECONDS, "00:05:00",      "" ],
    ])

displayTableInWidget(widget, table_scan)
