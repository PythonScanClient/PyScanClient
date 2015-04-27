"""
Initialize scan GUI
@author: Kay Kasemir
"""

from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.eclipse.jface.dialogs import MessageDialog

from errors import showException

try:
    from beamline_setup import *

    widget = display.getWidget("device1")
    widget.setPropertyValue("items", scan_settings.settable)
        
    widget = display.getWidget("cond_device")
    widget.setPropertyValue("items", scan_settings.waitable)
    
    widget = display.getWidget("log_device")
    widget.setPropertyValue("items", scan_settings.loggable)
except Exception, e:
    showException("Sorry...")

