"""
Load TableScan from file into Table widget
@author: Kay Kasemir
"""
from org.csstudio.display.builder.runtime.script import ScriptUtil, ValueUtil
from errors import showException
from tablescan_ui import getTableFromPath, displayTableInWidget

try:
    path = ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "TableFile"))
    table_scan = getTableFromPath(path)
    displayTableInWidget(widget, table_scan)
except:
    showException(widget, "Sorry...")

