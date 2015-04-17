'''
This is an example how to use PyScanClient library to perform a 2D scan using ndim scan.
It needs an example EPICS database, simulation.db, which could be found at: 
https://github.com/ControlSystemStudio/cs-studio/blob/master/applications/plugins/org.csstudio.scan/examples/
And it assumes the server running on localhost at port 4810.


It does the following:
    - set pv 'motor_x' to 1, which means to open a shutter, and wait until finish.
    - loop pv 'motor_x' from 1 to 5 with stepping size = 1 and wait until finish. at each step:
        - loop pv 'motor_y' from 1 to 3 with stepping size = 1, and wait until finish. at each step:
            - wait for 1 second
            - log pv 'motor_x', 'motor_y' and 'neutrons'
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
from scan import createNDimScan as ndim

from scan.commands import Comment, Delay, Set

from scan.client.logdata import createTable


if __name__ == '__main__':
    orig_motor_x = 0
    orig_motor_y = 0
    
    cmds = ndim(Comment("Example"),
                Set('motor_x', 1),
                ('motor_x', 1, 5, 1),
                ('motor_y', 1, 3, 1),
                Set('neutrons', 0, completion=True, readback=False),
                Delay(1), 'neutrons', 'setpoint')
    try:
        client = ScanClient('localhost', 4810)
        scid = client.submit(cmds, name="2D ndim scan example")
        client.waitUntilDone(scid)
        print "Number of log calls: %d" % client.lastSerial(scid)
         
        # get raw data back as a Python dict 
        data = client.getData(scid)
        print data
         
        # Create table for motor_x, motor_y and neutrons
        table = createTable(data, 'motor_x', 'motor_y', 'neutrons', 'setpoint')
        print "Position X: ", table[0]
        print "Position Y: ", table[1]
        print "Counts   : ",  table[2]
        print "Setpoint : ",  table[3]
                 
        # Remove specific scan task
        client.delete(scid)
        # or Remove information for all completed scans
        client.clear()
    except:
        raise
