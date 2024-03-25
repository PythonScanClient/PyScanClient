'''
This is an example how to use PyScanClient library to connect a scan server, and ask scan server to set a value
to pv 'motor_x'.

This example needs an example EPICS database, PyScanClient/example/simulation.db 

@author: shen, Kay Kasemir
'''
from scan import ScanClient
from scan import Comment, Set

client = ScanClient('localhost')

# Assemble commands for a scan
# Much more on that later...
cmds = [ Comment('Hello'), Set('motor_x', 10) ]

# Optionally, request a simulation that shows
# how 'Include' and 'Loop' commands get expanded.
simulation = client.simulate(cmds)
print(simulation)

# Submit scan for execution
scid = client.submit(cmds, 'My First Scan')

# Fetch information about scan
info = client.scanInfo(scid)
print(info)

# Could poll scanInfo until info.isDone().
# Shortcut:
info = client.waitUntilDone(scid)
print(info)
