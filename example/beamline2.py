from beamline_setup import *

# Table
cmds = scan.table(
  [ 'xpos',    'ypos', 'Wait For', 'Value'],
[
  [     1, [ 2, 4, 6],  'pcharge',    3e9 ],
  [     3,          8,  'pcharge',    3e9 ],
])
print cmds
id = scan.submit(cmds)
# scan.waitUntilDone(id)

