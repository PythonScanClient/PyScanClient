"""
Submit alignment scan from widgets to scan server
@author: Kay Kasemir
"""
from org.csstudio.display.builder.runtime.script import ScriptUtil, ValueUtil
from beamline_setup import scan_client, Set
from scan.alignment import AlignmentScan
from scan.commands import CommandSequence
from errors import showException

try:
    device = str(ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "device1_1"))).strip()
    start = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "start1"))
    end = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "end1"))
    step = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "step1"))
    condition_device = str(ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "cond_device_1"))).strip()
    condition_value = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "cond_value"))
    log = str(ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "log_device_1"))).strip()
    method = str(ValueUtil.getString(ScriptUtil.getWidgetValueByName(widget, "method"))).strip()
    normalize = ValueUtil.getInt(ScriptUtil.getWidgetValueByName(widget, "normalize")) > 0

    if method=="Gauss":
        find_command = "FindPeak"
        name = "Gauss Scan of %s over %s" % (log, device)
    else:
        find_command = None
        name = "Range Scan of %s over %s" % (log, device)

    print(name)

    align = AlignmentScan(device, start, end, step, condition_device, condition_value, log,
                          start=[ Set('pcharge', 0) ],
                          find_command=find_command,
                          normalize=normalize)
    commands = CommandSequence(align.createScan())
    print(commands)
    scan_client.submit(commands, name=name)
except:
    showException(widget, "Alignment Scan")
