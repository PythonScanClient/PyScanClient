from beamline_setup import *

scan.ls()

# N-Dim scan
print scan.ndim(('xpos', 1, 10))
print scan.ndim(('xpos', 1, 10), Comment('New X'), ('ypos', 1, 3), TakeData('beam_monitor', 1e12), 'neutrons')

# Table
print scan.table( [ 'xpos', 'ypos',     'Wait For', 'Value'],
                [
                  [    1,   [ 2, 4, 6], 'counts'   ,  1000],
                  [    3,            8, 'counts'   ,  1000],
                ])

# Custom scan
cmds = CommandSequence()
cmds.append(scan_settings.Set('xpos', 1))
cmds.append(scan_settings.Set('ypos', 1))
cmds.append(SetChopper(1.7, 45.0))
cmds.append(TakeData('counts', 1000))
print cmds
