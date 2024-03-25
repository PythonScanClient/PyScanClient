'''
This is an example how to use PyScanClient library to perform a 2D scan using basic command, and take multiple samples
at each point.

It does the following:
    - loop pv 'motor_x' from 1 to 5 with stepping size = 1 and wait until finish. at each step:
        - loop pv 'motor_y' from 1 to 3 with stepping size = 1, and wait until finish. at each step:
            - wait for 1 second
            - log multiple samples for pv 'motor_x', 'motor_y' and 'neutrons'
    - get logged data back
    - create a table for the results
    - clear scan server

@author: shen, Kay Kasemir
'''
from scan.client.scanclient import ScanClient
from scan.commands import Set, Loop, Delay, Log, Comment

from scan.client.logdata import createTable

cmds = [Comment("Example"),
        Loop('motor_x', 1, 5, 1,
                [Loop('motor_y', 1, 3, 1,
                    [Loop('loc://i(0)', 
                            1, 2, 1, 
                            [Delay(1),
                            Log('motor_x', 'motor_y', 'neutrons')
                            ]),
                    ]),
                ])
        ]
client = ScanClient('localhost', 4810)
scid = client.submit(cmds, name="2D scan example")
client.waitUntilDone(scid)
print("Number of log calls: %d" % client.lastSerial(scid))

# get raw data back as a Python dict 
data = client.getData(scid)

# Create table for motor_x, motor_y and neutrons
table = createTable(data, 'motor_x', 'motor_y', 'neutrons')
print("Position X: ", table[0])
print("Position Y: ", table[1])
print("Counts   : ",  table[2])
        
# Remove specific scan task
#client.delete(scid)
# or Remove information for all completed scans
#client.clear()
