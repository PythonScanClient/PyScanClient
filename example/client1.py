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

# Could poll scanInfo until scan is done
info = client.scanInfo(id)
print info

# Shortcut for waiting until it'd done
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

# get commands

# get data


# Remove information for all completed scans
client.clear()
