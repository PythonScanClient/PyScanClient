from beamline_setup import *

# Custom scan
cmds = CommandSequence()
cmds.append(Set('xpos', 1))
cmds.append(Set('ypos', 1, completion=False))
cmds.append(SetChopper(1.7, 45.0))
cmds.append(TakeData('pcharge', 5e9))
print cmds
id = scan.submit(cmds)
print "Submitted scan #%d" % id


