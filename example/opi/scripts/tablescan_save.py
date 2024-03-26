"""
Save TableScan from widget to file
@author: Kay Kasemir
"""
from org.csstudio.display.builder.runtime.script import ScriptUtil, ValueUtil
from errors import showException
from tablescan_ui import saveTableFromWidget

path = ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "TableFile"))

try:
    saveTableFromWidget(widget, path)
except:
    showException(widget, "Table Save Error")       
