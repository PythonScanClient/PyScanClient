import time
from scan import *
  
client = ScanClient('localhost')
print client

print client.serverInfo()

# Assemble commands for a scan
# Much more on that later...
cmds = [ Comment('Hello'), Set('motor_x', 10) ]

# Optionally, request a simulation that shows
# how 'Include' and 'Loop' commands get expanded.
simulation = client.simulate(cmds)
print simulation

# Submit scan for execution
id = client.submit(cmds, 'My First Scan')
print id

# Fetch information about scan
info = client.scanInfo(id)
print info

# Could poll scanInfo until info.isDone().
# Shortcut:
info = client.waitUntilDone(id)
print info

# A submitted scan can be paused..
id = client.submit(cmds, 'Not sure about this one')

client.pause(id)
print client.scanInfo(id)

client.resume(id)
print client.scanInfo(id)

# .. or even aborted  & deleted
client.abort(id)
print client.scanInfo(id)

print "Before deleting scan %d:" % id, [ str(info) for info in client.scanInfos() ]
client.delete(id)
print "After  deleting scan %d:" % id, [ str(info) for info in client.scanInfos() ]

# In extreme cases, it is possible to change a running scan
id = client.submit([ Delay(5), Set('motor_x', 10) ], 'Changing...')
client.pause(id)
# Want to set 'motor_x' to 5 instead of 10
client.patch(id, 1, 'value', 5)
client.resume(id)
client.abort(id)

try:
    client.waitUntilDone(id)
except Exception, e:
    print "Waiting for an aborted scan will result in an exception: ", e

try:
    # This scan will time out
    id = client.submit( [ Wait("motor_x", 60, timeout=1)], "Timeout Test")
    client.waitUntilDone(id)
except Exception, e:
    print "Waiting for a failed scan will result in an exception: ", e

# Log data during scan
cmds = [ Loop('motor_x', 1, 10, 1,
              [ 
                  Set('neutrons', 0),
                  Loop('motor_y', 1, 3, 1,
                       [
                           Delay(1),
                           Log('motor_y')
                       ]),
                  Log('motor_x', 'neutrons')
              ])
       ]
id = client.submit(cmds, 'Data Demo')
info = client.waitUntilDone(id)
print "Number of log calls: %d" % client.lastSerial(id)

# Fetch data
data = client.getData(id)
 
# Create table for motor_x and neutrons
table = createTable(data, 'motor_x', 'neutrons')
print "Positions: ", table[0]
print "Counts   : ", table[1]
for (pos, count) in zip(*table):
    print "Counts at motor position %g: %g" % (pos, count)
    
# Could plot this with numpy/scipy:  plot(table[0], table[1]) etc.

# TODO get commands back from server

# Remove information for all completed scans
client.clear()
