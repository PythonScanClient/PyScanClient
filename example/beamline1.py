from beamline_setup import *

scan.ls()

# N-Dim scan
cmds = scan.ndim(('xpos', 1, 10), Delay(0.2))
print cmds
id = scan.submit(cmds)
scan.waitUntilDone(id)

# In simulation, pcharge rises at about 1e9 per second
cmds = scan.ndim(('xpos', 1, 3), ('ypos', 1, 3), Wait('pcharge', 3e9), 'pcharge', 'neutrons')
print cmds
id = scan.submit(cmds)
scan.waitUntilDone(id)


# Table
print scan.table( [ 'xpos', 'ypos',     'Wait For', 'Value'],
                [
                  [    1,   [ 2, 4, 6], 'counts'   ,  1000],
                  [    3,            8, 'counts'   ,  1000],
                ])

# Custom scan
cmds = CommandSequence()
cmds.append(Set('xpos', 1))
cmds.append(Set('ypos', 1, completion=False))
cmds.append(SetChopper(1.7, 45.0))
cmds.append(TakeData('counts', 1000))
print cmds



