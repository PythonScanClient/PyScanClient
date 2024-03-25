'''
This is an example how to use PyScanClient library to perform a 2D scan using table scan

In addition to the basic table scan operations, it uses

pre to move some motor, assuming that would be a motor that opens a shutter

post to restore motor positions

start to do something at each "Wait For" step

@author: shen, Kay Kasemir
'''

from scan.client.scanclient import ScanClient
from scan.table import TableScan


from scan.client.logdata import createTable

from scan.util.scan_settings import ScanSettings, setScanSettings
# Note how we replace the original Set() and Wait() commands with those that utilize ScanSettings
from scan.util.scan_settings import SettingsBasedSet as Set

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

orig_motor_x = 0
orig_motor_y = 0

# Custom settings configure the TableScan
setScanSettings(LocalScanSettings())
# Create table scan command
# use function to generate scan range
table = TableScan(['Comment',     'motor_x',       'motor_y',     'loc://i(0)',     'Wait For',   'Value'],
                    [['Example',       '',              '',             '',               '',         ''], 
                    ['',        'range(1, 6, 1)', 'range(1, 4, 1)','range(1, 3, 1)',  'Seconds',      1],
                    ['',               1,                1,           '',                '',         '']],
                    pre=Set('motor_x', 1, completion=True),
                    post=[Set('motor_x', orig_motor_x, completion=True),
                        Set('motor_y', orig_motor_y, completion=True),],
                    start=Set("neutrons", 0, completion=True, timeout=10),
                    log_always=('neutrons', 'setpoint')
                    )

cmds = table.createScan()

client = ScanClient('localhost', 4810)
scid = client.submit(cmds, name="2D table scan example")
client.waitUntilDone(scid)
    
# get raw data back as a Python dict 
data = client.getData(scid)
    
# Create table for motor_x, motor_y and neutrons
table = createTable(data, 'motor_x', 'motor_y', 'neutrons', 'setpoint')
print("Position X: ", table[0])
print("Position Y: ", table[1])
print("Counts   : ",  table[2])
print("Setpoint : ",  table[3])
            
# Remove specific scan task
#client.delete(scid)
# or Remove information for all completed scans
#client.clear()
