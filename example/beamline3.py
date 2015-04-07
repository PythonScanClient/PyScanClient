from beamline_setup import *

# Custom scan
cmds = CommandSequence()
cmds.append(Set('xpos', 1))
cmds.append(Set('ypos', 1, completion=False))
cmds.append(Set('setpoint', 8))
cmds.append(SetChopper(1.7, 45.0))
cmds.append(TakeData('pcharge', 5e9))
cmds.append(Set('setpoint', 1))
print cmds

result = scan_client.simulate(cmds)
print result['simulation']

id = scan_client.submit(cmds)
print "Submitted scan #%d" % id


