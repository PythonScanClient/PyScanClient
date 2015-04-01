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

# Log data during scan
id = client.submit([ Loop('motor_x', 1, 10, 1,
                      [ Log('motor_x'),
                        Loop('motor_y', 1, 3, 1,
                              Log('motor_y'))
                      ])
                   ], 'Data Demo')
info = client.waitUntilDone(id)
print "Number of log calls: %d" % client.lastSerial(id)

# TODO Details under development
# 
# # Direct access to data dict
# print "Values: ", data['motor_x']['value']
# print "Times: ", data['motor_x']['time']
# 
# # Convert times in posix millisecs into local datatime
# print "Times: ", [ str(getDatetime(time)) for time in  data['motor_x']['time'] ]
# 
# # Demo of sample iterator
# for s in SampleIterator(data, 'motor_x'):
#     print "%s (%2d): %s" % (str(getDatetime(s[1])), s[0], str(s[2]))
# 
# # Create table, i.e. align samples for different devices by sample ID:    
# table = createTable(data, 'motor_x', 'motor_y')
# print table[0]
# print table[1]
# # With numpy/scipy:  plot(table[0], table[1]) etc.

# TODO get commands back from server

# Remove information for all completed scans
client.clear()
