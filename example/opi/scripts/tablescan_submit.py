"""
Submit TableScan from Table widget to scan server
@author: Kay Kasemir
"""
from errors import showException
from tablescan_ui import getTableFromWidget
from beamline_setup import scan_client

try:
    table_scan = getTableFromWidget(display)
    
    name = display.getWidget("TableFile").getValue().strip()
    if name:
        table_scan.name = name

    if table_scan:
        commands = table_scan.createScan()
        id = scan_client.submit(commands, name=name)
except:
    showException("Table Scan")
