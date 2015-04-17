'''
This is an example how to use PyScanClient library to perform a 2D scan using table scan.
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
from scan.table import TableScan

# from scan.commands import Comment
# from scan.commands import Set
# from scan.commands import Loop
# from scan.commands import Delay
from scan.commands import Log

from scan.client.logdata import createTable

from scan.util.scan_settings import ScanSettings, setScanSettings
# Note how we replace the original Set() and Wait() commands with those that utilize ScanSettings
from scan.util.scan_settings import SettingsBasedSet as Set
# from scan.util.scan_settings import SettingsBasedWait as Wait
# from scan.util.scan_settings import SettingsBasedLoop as Loop

class LocalScanSettings(ScanSettings):
    """Example for site-specific scan settings."""
    def __init__(self):
        super(LocalScanSettings, self).__init__()

        # use motor, and does not check its readback
        self.defineDeviceClass(".*motor.*", completion=True, readback=False, timeout=10)
#         
#     def getReadbackName(self, device_name):
#         # Motors use their *.RBV field for readback
#         if 'motor' in device_name:
#             return device_name + ".RBV"
#         return device_name

if __name__ == '__main__':
    orig_motor_x = 0
    orig_motor_y = 0
    
    # Custom settings configure the TableScan
    setScanSettings(LocalScanSettings())
    # Create table scan command
    # list all scan parameters
    table = TableScan(['motor_x', 'motor_y', "Wait For", "Value"],
                      [ [  1,        1,       'Seconds',   1],
                        [ '',        2,       'Seconds',   1],
                        [ '',        3,       'Seconds',   1],
                        [  2,        1,       'Seconds',   1],
                        [ '',        2,       'Seconds',   1],
                        [ '',        3,       'Seconds',   1],
                        [  3,        1,       'Seconds',   1],
                        [ '',        2,       'Seconds',   1],
                        [ '',        3,       'Seconds',   1],
                        [  4,        1,       'Seconds',   1],
                        [ '',        2,       'Seconds',   1],
                        [ '',        3,       'Seconds',   1],
                        [  5,        1,       'Seconds',   1],
                        [ '',        2,       'Seconds',   1],
                        [ '',        3,       'Seconds',   1],], 
                    pre=Set('motor_x', 1, completion=True),
                    post=[Set('motor_x', orig_motor_x, completion=True),
                          Set('motor_y', orig_motor_y, completion=True),],
                    log_always=('neutrons', 'setpoint'))
    cmds = table.createScan()
    try:
        client = ScanClient('localhost', 4810)
        scid = client.submit(cmds, name="2D table scan example")
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
