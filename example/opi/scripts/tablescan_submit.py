"""
Submit TableScan from Table widget to scan server
@author: Kay Kasemir
"""
from org.csstudio.display.builder.runtime.script import ScriptUtil, ValueUtil
from errors import showException
from tablescan_ui import getTableFromWidget
from beamline_setup import scan_client

try:
    table_scan = getTableFromWidget(widget)
    
    path = ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "TableFile"))
    name = path.strip()
    if name:
        table_scan.name = name

    commands = table_scan.createScan()
    id = scan_client.submit(commands, name=name)
except:
    showException(widget, "Table Scan")
