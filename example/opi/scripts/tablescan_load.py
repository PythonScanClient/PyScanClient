"""
Load TableScan from file into Table widget
@author: Kay Kasemir
"""
from errors import showException
from tablescan_ui import getTableFromPath, displayTableInWidget

try:
    path = display.getWidget("TableFile").getValue()
    table_scan = getTableFromPath(path)
    displayTableInWidget(display, table_scan)
except:
    showException("Sorry...")

