'''
This is an example how to use PyScanClient library to perform a 1D scan, and take multiple samples at each point.

It does the following:
    - loop pv 'motor_x' from 1 to 10 with stepping size = 1 and wait until finish. at each step:
        - wait for 1 second
        - log 3 values for pv 'motor_x' and 'neutrons'
    - get logged data back
    - create a table for the results
    - clear scan server

@author: shen, Kay Kasemir
'''

from scan.client.scanclient import ScanClient
from scan.commands import Set, Loop, Delay, Log, Comment

from scan.client.logdata import createTable

client = ScanClient('localhost', 4810)
cmds = [Comment("Example"),
        Loop('motor_x', 1, 5, 1,
                [Loop('loc://i(0)', 1, 3, 1,  
                    [Log('motor_x', 'neutrons'), 
                    Delay(1)]
                    )
                ],
                completion=True
                )
        ]
    
scid = client.submit(cmds, name="1D scan example")
client.waitUntilDone(scid)
data = client.getData(scid)
import pprint
pprint.pprint(data)

# Create table for motor_x and neutrons
table = createTable(data, 'motor_x', 'neutrons')
print("Positions: ", table[0])
print("Counts   : ", table[1])

# Remove specific scan task
#client.delete(scid)
# or Remove information for all completed scans
#client.clear()
