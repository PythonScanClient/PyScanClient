from scan.client.scanclient import ScanClient

from scan.commands import *
  
client = ScanClient('localhost')
print client
 
cmds = [ Comment('Hello'), Set('x', 10) ]

# Optionally, request a simulation that shows
# how 'Include' and 'Loop' commands get expanded.
simulation = client.simulate(cmds)
print simulation

id = client.submit(cmds, 'My First Scan')
print id



# TODO info

# get commands

# get data

# delete