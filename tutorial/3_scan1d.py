'''
This is an example how to use PyScanClient library to perform a 1D scan.
It needs an example EPICS database, simulation.db

It does the following:
    - set pv 'motor_x' to 1, which means to open a shutter, and wait until finish.
    - loop pv 'motor_x' from 1 to 10 with stepping size = 1 and wait until finish. at each step:
        - wait for 1 second
        - log pv 'motor_x' and 'neutrons'
    - set pv 'motor_x' to original place 
    - get logged data back
    - create a table for the results
    - clear scan server

It does not demo:
    - read back and its tolerance to ensure 

@author: shen, Kay Kasemir
'''

from scan.client.scanclient import ScanClient
from scan.commands import Set, Loop, Delay, Log, Comment

from scan.client.logdata import createTable

orig_motor = 0
client = ScanClient('localhost', 4810)
cmds = [Comment("Example"),
        Set('motor_x', 1, completion=True),
        Loop('motor_x', 1, 10, 1,
                [
                Delay(1.0),
                Log("motor_x","neutrons")
                ], 
                completion=True),
        Set('motor_x', orig_motor, completion=True)
        ]
    
scid = client.submit(cmds, name="1D scan example")
client.waitUntilDone(scid)
data = client.getData(scid)

# Create table for motor_x and neutrons
table = createTable(data, 'motor_x', 'neutrons')
print("Positions: ", table[0])
print("Counts   : ", table[1])
        
# Remove specific scan task
client.delete(scid)
# or Remove information for all completed scans
client.clear()
