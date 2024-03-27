"""
Initialize alignment scan GUI
@author: Kay Kasemir
"""

from org.csstudio.display.builder.runtime.script import ScriptUtil, PVUtil
from errors import showException

try:
    from beamline_setup import *

    # Populate combo options, default to the first option
    combo = ScriptUtil.findWidgetByName(widget, "device1")
    combo.setItems(scan_settings.settable)
    pv = ScriptUtil.getPrimaryPV(combo)
    if len(PVUtil.getString(pv)) <= 0:
        pv.write(scan_settings.settable[0])

    combo = ScriptUtil.findWidgetByName(widget, "cond_device")
    combo.setItems(scan_settings.waitable)
    pv = ScriptUtil.getPrimaryPV(combo)
    if len(PVUtil.getString(pv)) <= 0:
        pv.write(scan_settings.waitable[0])

    combo = ScriptUtil.findWidgetByName(widget, "log_device")
    combo.setItems(scan_settings.loggable)
    pv = ScriptUtil.getPrimaryPV(combo)
    if len(PVUtil.getString(pv)) <= 0:
        pv.write(scan_settings.loggable[0])

except Exception, e:
    showException(widget, "Sorry...")

