'''
This is an example how to use PyScanClient library to perform a 2D scan using basic command, and take multiple samples
at each point.
It needs an example EPICS database, simulation.db, which could be found at: 
https://github.com/ControlSystemStudio/cs-studio/blob/master/applications/plugins/org.csstudio.scan/examples/
And it assumes the server running on localhost at port 4810.


It does the following:
    - set pv 'motor_x' to 1, which means to open a shutter, and wait until finish.
    - loop pv 'motor_x' from 1 to 5 with stepping size = 1 and wait until finish. at each step:
        - loop pv 'motor_y' from 1 to 3 with stepping size = 1, and wait until finish. at each step:
            - wait for 1 second
            - log multiple samples for pv 'motor_x', 'motor_y' and 'neutrons'
    - set pv 'motor_x' to original place
    - set pv 'motor_y' to original place 
    - get logged data back
    - create a table for the results
    - clear scan server

It does not demo:
    - read back and its tolerance to ensure 

Created on Apr 17, 2015

@author: shen
'''
from scan.client.scanclient import ScanClient
from scan.commands import Set, Loop, Delay, Log, Comment

from scan.client.logdata import createTable

if __name__ == '__main__':
    orig_motor_x = 0
    orig_motor_y = 0
    try:
        cmds = [Comment("Example"),
                Set('motor_x', 1, completion=True), 
                Loop('motor_x', 1, 5, 1,
                     [Loop('motor_y', 1, 3, 1,
                           [Loop('loc://i(0)', 
                                 1, 2, 1, 
                                 [Delay(1),
                                  Log('motor_x', 'motor_y', 'neutrons')
                                  ]),
                            ]),
                     ]),
                Set('motor_x', orig_motor_x, completion=True),
                Set('motor_y', orig_motor_y, completion=True)
               ]
        for cmd in cmds:
            print cmd
        exit()
        client = ScanClient('localhost', 4810)
        scid = client.submit(cmds, name="2D scan example")
        client.waitUntilDone(scid)
        print "Number of log calls: %d" % client.lastSerial(scid)
        
        # get raw data back as a Python dict 
        data = client.getData(scid)
        
        # Create table for motor_x, motor_y and neutrons
        table = createTable(data, 'motor_x', 'motor_y', 'neutrons')
        print "Position X: ", table[0]
        print "Position Y: ", table[1]
        print "Counts   : ",  table[2]
                
        # Remove specific scan task
        client.delete(scid)
        # or Remove information for all completed scans
        client.clear()
    except:
        raise
