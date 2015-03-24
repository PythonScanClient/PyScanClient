"""Unit test of the TableScan

   @author: Kay Kasemir
"""
import unittest
from scan.table import TableScan
from scan.util.scan_settings import ScanSettings

class MyScanSettings(ScanSettings):
    def __init__(self):
        super(MyScanSettings, self).__init__()
        # Define special settings for some devices
        self.defineDeviceClass("Motor.*", completion=True, readback=True, timeout=100)
        
    def getReadbackName(self, device_name):
        # Motors use their *.RBV field for readback
        if "Motor" in device_name:
            return device_name + ".RBV"
        return device_name

# TODO Check the generated scan once the string representation of commands is fixed
# TODO WaitFor, Value
# TODO Open/close shutter
# TODO 'Comment' column can be comment command or Set('SomeCommentPV')
# TODO Start/stop DAQ, overall or on each 'line'
# TODO Reset counters, issue scan step markers
# TODO Devices to always log
# TODO Devices where we need to await 'increment' instead of absolute value 
# TODO Start by waiting for all motors to be idle
#         for motor in motors:
#             idle = self.settings.getMotorIdlePV(motor)
#             if idle:
#                 commands.insert(0, WaitCommand(idle, Comparison.EQUALS, 1, 0.1, 5.0))

settings = MyScanSettings()

def handle(table):
    print table
    cmds = table.createScan()
    print
    for cmd in cmds:
        print str(cmd)
    return cmds


class TableScanTest(unittest.TestCase):
    def testBasics(self):
        print "\n=== Basic Table ==="
        table_scan = TableScan(settings,
          (   "Comment", "X ",  "Y", "Speed", "Wavelength" ),
          [
            [ "Setup",  "  1",  "2",    "30",           "" ],
            [ "Count",     "",   "",      "",        "100" ],
            [ "Wait",      "",   "",      "",        "200" ],
          ]
        )
        cmds = handle(table_scan)
        #self.assertEqual(str(cmds), "[Comment('Setup'), Set(device='X',value=1.0), Set(device='Y',value=2.0), Set(device='Speed',value=30.0), Comment('Count'), Set(device='Wavelength',value=100.0), Comment('Wait'), Set(device='Wavelength',value=200.0)]")


    def testScanSettings(self):
        print "\n=== ScanSettings configure Motor for completion and RBV ==="
        table_scan = TableScan(settings,
          (   "X ",  "Motor1" ),
          [
            [ "  1",  "2" ],
          ]
        )
        cmds = handle(table_scan)
        # self.assertEqual(str(cmds), "")


        print "\n=== Override ScanSettings for Motor ==="
        table_scan = TableScan(settings,
          (   "Motor1",  "-cr Motor2" ),
          [
            [ "  1",  "2" ],
          ]
        )
        cmds = handle(table_scan)
        # self.assertEqual(str(cmds), "")


    def testParallel(self):
        print "\n=== Parallel ==="
        table_scan = TableScan(settings,
          (   "X", "+p Y", "+p Z" ),
          [
            [ "1", "2",    "3" ],
          ]
        )
        cmds = handle(table_scan)
        # self.assertEqual(str(cmds), "")


    def testRange(self):
        print "\n=== Range Cells ==="
        table_scan = TableScan(settings,
          (   " X ",  "Y", ),
          [
            [ "  1",  "", ],
            [ "   ",  "range(5)", ],
            [ "[ 0, 1]", "range(2)", ],
          ]
        )
        cmds = handle(table_scan)
        # self.assertEqual(str(cmds), "[Set(device='X',value=1.0), Set(device='Y',value=0.0), Set(device='Y',value=1.0), Set(device='Y',value=2.0), Set(device='Y',value=3.0), Set(device='Y',value=4.0), Set(device='X',value=0.0), Set(device='Y',value=0.0), Set(device='X',value=0.0), Set(device='Y',value=1.0), Set(device='X',value=1.0), Set(device='Y',value=0.0), Set(device='X',value=1.0), Set(device='Y',value=1.0)]")



if __name__ == "__main__":
    unittest.main()