from beamline_setup import *

# Table
cmds = table_scan(
  [ 'motor_x', 'motor_y', 'Wait For', 'Value'],
[
  [         1, [ 2, 4, 6], 'pcharge',  3*1e9 ],
  [         3,          8, 'pcharge',  3*1e9 ],
])
print(CommandSequence(cmds))
id = scan_client.submit(cmds)
scan_client.waitUntilDone(id)

# Dump motor positions
data = scan_client.getData(id)
table = createTable(data, 'motor_x', 'motor_y')
for (x, y) in zip(*table):
    print("%d, %d" % (x, y))
