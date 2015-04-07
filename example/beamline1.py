from beamline_setup import *

# N-Dim scan
cmds = scan_client.ndim(('xpos', 1, 10), Delay(0.2))
print cmds
id = scan_client.submit(cmds)
scan_client.waitUntilDone(id)

# Simulated pcharge rises at about 1e9 per second
cmds = scan_client.ndim(('xpos', 1, 3), ('ypos', 1, 3), TakeData('pcharge', 3*1e9), 'neutrons')
print cmds
id = scan_client.submit(cmds)
# scan_client.waitUntilDone(id)
