"""
Helpers for TableScan and UI
@author: Kay Kasemir
"""

from beamline_setup import scan_settings
from scan.table.table_scan import loadTableScan, TableScan

from org.eclipse.core.resources import ResourcesPlugin
from org.eclipse.core.runtime import Path

from array import array
from java.lang import String
from org.csstudio.swt.widgets.natives import SpreadSheetTable
from org.csstudio.opibuilder.scriptUtil import FileUtil

def getTableFromPath(path):
    path = FileUtil.workspacePathToSysPath(path)
    if path:
        return loadTableScan(path)
    else:
        raise Exception("No file to load")

def saveTableFromWidget(display, path):
    if path is None  or  len(path) <= 0:
        raise Exception("Invalid or empty file name")
    path = FileUtil.workspacePathToSysPath(path)
    if path is None:
        raise Exception("Save Error", "Invalid file name or path")       
    table_scan = getTableFromWidget(display)
    table_scan.save(path)
    # Force a workspace refresh on the new file
    ResourcesPlugin.getWorkspace().getRoot().getFileForLocation(Path(path)).refreshLocal(0, None)

def getTableFromWidget(display):
    """Create table scan from table widget
    :param display: Display
    :return: TableScan
    """
    widget = display.getWidget("TableScan")
    table = widget.getTable()
    headers = table.getColumnHeaders()
    rows = table.getContent()
    return TableScan(headers, rows)


def displayTableInWidget(display, table_scan):
    """Display table scan in table widget
    :param display: Display
    :param table_scan: TableScan
    """
    cols = len(table_scan.headers)
    widget = display.getWidget("TableScan")
    table = widget.getTable()
    table.setColumnHeaders(table_scan.headers)
    table.setColumnsCount(cols)
    
    # Copy the actual table, adding extra empty rows to
    # simplify editing (entering new scan rows)
    rows = []
    for row in table_scan.rows:
        rows.append(row)
    empty = []
    for col in range(cols):
        empty.append("")
    for extra in range(10):
        rows.append(empty)
    table.setContent(rows)

    # Size table columns to fill width of widget
    width = widget.getPropertyValue("width") - 50
    for c in range(cols):
        table.setColumnWidth(c, width/cols)

    # Some columns need special editor
    for c in range(cols):
        if table_scan.headers[c] == table_scan.WAITFOR:
            table.setColumnCellEditorType(c, SpreadSheetTable.CellEditorType.DROPDOWN)
            table.setColumnCellEditorData(c, array(String, scan_settings.waitable))
        else:
            table.setColumnCellEditorType(c, SpreadSheetTable.CellEditorType.TEXT)

