"""
Helpers for TableScan and UI
@author: Kay Kasemir
"""

from beamline_setup import scan_settings, Start, Stop, Pre, Post
from org.csstudio.display.builder.runtime.script import ScriptUtil

from scan.table.table_scan import loadTableScan, TableScan

def getTableFromPath(path):
    return loadTableScan(path)

def getTableFromWidget(widget):
    """Create table scan from table widget
    :param widget: Any widget in the display
    :return: TableScan
    """
    table = ScriptUtil.findWidgetByName(widget, "TableScan")
    headers = table.getHeaders()
    rows = table.getValue()
    return TableScan(headers, rows, pre=Pre(), post=Post(), start=Start(), stop=Stop())

def saveTableFromWidget(widget, path):
    table_scan = getTableFromWidget(widget)
    table_scan.save(path)

def displayTableInWidget(widget, table_scan):
    """Display table scan in table widget
    :param widget: Any widget, sibling of table
    :param table_scan: TableScan
    """
    # Locate table widget
    table = ScriptUtil.findWidgetByName(widget, "TableScan")
    # Show table
    table.setHeaders(table_scan.headers)
    table.setValue(table_scan.rows)
    # Update table column details
    for c in range(len(table_scan.headers)):
        if table_scan.headers[c] == table_scan.WAITFOR:
            table.setColumnOptions(c, scan_settings.waitable)
