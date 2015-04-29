"""
Schedule scan with parameters from BOY script

@author: Kay Kasemir
"""
from org.csstudio.scan.ui import SimulationDisplay
from org.csstudio.scan.server import SimulationResult

from org.eclipse.ui import PlatformUI


from errors import showException

from scan.commands.loop import Loop
from scan.commands.wait import Wait
from scan.commands.log import Log
from beamline_setup import scan_client

try:
    # Fetch parameters from display
    x0 = float(display.getWidget("x0").getValue())
    x1 = float(display.getWidget("x1").getValue())
    dx = float(display.getWidget("dx").getValue())
    y0 = float(display.getWidget("y0").getValue())
    y1 = float(display.getWidget("y1").getValue())
    dy = float(display.getWidget("dy").getValue())
    neutrons = float(display.getWidget("neutrons").getValue())
    simu = str(display.getWidget("simu").getValue()) == "True"
    if str(display.getWidget("updown").getValue()) == "True":
        toggle = -1
    else:
        toggle = 1
    
    #from org.eclipse.jface.dialogs import MessageDialog
    #MessageDialog.openWarning(
    #        None, "Type", "Type is " + neutrons.__class__.__name__)       
    
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
        simulation = scan_client.simulate(cmds)
        SimulationDisplay.show(SimulationResult(simulation['seconds'], simulation['simulation']))
    else:
        # Submit scan
        id = scan_client.submit(cmds, "XY Scan")
        workbench = PlatformUI.getWorkbench()
        window = workbench.getActiveWorkbenchWindow()
        page = window.getActivePage()
        plot = page.showView("org.csstudio.scan.ui.plot.view")
        plot.selectScan("XY Scan", id)
        plot.selectDevices("xpos", "ypos")
except:
    showException("XY Scan")
