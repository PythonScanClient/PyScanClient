"""
Save TableScan from widget to file
@author: Kay Kasemir
"""
from tablescan_ui import saveTableFromWidget
from errors import showException

path = display.getWidget("TableFile").getValue()
try:
    saveTableFromWidget(display, path)
except:
    showException("Table Save Error")       
