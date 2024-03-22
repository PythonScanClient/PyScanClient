"""
Schedule scan with parameters from BOY script

@author: Kay Kasemir
"""

from org.csstudio.display.builder.runtime.script import ScriptUtil, ValueUtil
from java.lang import Runnable
from javafx.application import Platform
from org.csstudio.scan.info import SimulationResult
from org.phoebus.framework.workbench import ApplicationService
from scan.commands.loop import Loop
from scan.commands.wait import Wait
from scan.commands.log import Log
from scan.client import ScanClient

# Fetch parameters from display
x0 = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "x0"))
x1 = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "x1"))
dx = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "dx"))
y0 = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "y0"))
y1 = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "y1"))
dy = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "dy"))
neutrons = ValueUtil.getDouble(ScriptUtil.getWidgetValueByName(widget, "neutrons"))
simu = ValueUtil.getInt(ScriptUtil.getWidgetValueByName(widget, "simu")) > 0
if ValueUtil.getInt(ScriptUtil.getWidgetValueByName(widget, "updown")) > 0:
    toggle = -1
else:
    toggle = 1
    
# Create scan
cmds =[
  Loop('xpos', min(x0, x1), max(x0, x1), max(0.1, abs(dx)),
    Loop('ypos', min(y0, y1), max(y0, y1), toggle * max(0.1, abs(dy)),
    [
        Wait('neutrons', neutrons, comparison='increase by'),
        Log('xpos', 'ypos', 'readback')
    ]
    )
  )
]

if simu:
    sim = ScanClient().simulate(cmds)

    class ShowSimulation(Runnable):
        def __init__(self, result):
            self.result = SimulationResult(result['seconds'], result['simulation'])
        def run(self):
            inst = ApplicationService.createInstance("scan_simulation")
            inst.show(self.result)
    
    Platform.runLater(ShowSimulation(sim))
else:
    # Submit scan
    scan_id = ScanClient().submit(cmds, "XY Scan")
