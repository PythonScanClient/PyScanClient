"""
Submit alignment scan from widgets to scan server
@author: Kay Kasemir
"""
from beamline_setup import scan_client
from scan.commands.set import Set
from scan.alignment import AlignmentScan
from errors import showException

try:
    device = str(display.getWidget("device1_1").getValue()).strip()
    start = float(display.getWidget("start1").getValue())
    end = float(display.getWidget("end1").getValue())
    step = float(display.getWidget("step1").getValue())
    condition_device = str(display.getWidget("cond_device_1").getValue()).strip()
    condition_value = float(display.getWidget("cond_value").getValue())
    log = str(display.getWidget("log_device_1").getValue()).strip()
    method = str(display.getWidget("method").getValue()).strip()
    normalize = bool(display.getWidget("normalize").getValue())

    if method=="Gauss":
        find_command = "FindPeak"
        name = "Gauss Scan of %s over %s" % (log, device)
    else:
        find_command = None
        name = "Range Scan of %s over %s" % (log, device)
    
    align = AlignmentScan(device, start, end, step, condition_device, condition_value, log,
                          start=[ Set('pcharge', 0) ],
                          find_command=find_command,
                          normalize=normalize)
    scan_client.submit(align.createScan(), name=name)
except:
    showException("Alignment Scan")
