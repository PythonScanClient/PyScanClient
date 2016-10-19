"""Unit test of the TableScan

   @author: Kay Kasemir
"""
import unittest
from scan.commands import Set, Comment, Delay
from scan.table import TableScan
from scan.util import ScanSettings, setScanSettings
from scan.commands.include import Include
from scan.util.seconds import parseSeconds


class MyScanSettings(ScanSettings):
    def __init__(self):
        super(MyScanSettings, self).__init__()
        # Define special settings for some devices
        self.defineDeviceClass("Motor.*", completion=True, readback=True, timeout=100)
        self.defineDeviceClass("InfiniteCounter", comparison="increase by")
        
    def getReadbackName(self, device_name):
        # Motors use their *.RBV field for readback
        if "Motor" in device_name:
            return device_name + ".RBV"
        return device_name

setScanSettings(MyScanSettings())

# TODO 'Comment' column can be comment command or Set('SomeCommentPV')
# TODO Fix Log command
# TODO Devices to always log
# TODO Start by waiting for all motors to be idle
#         for motor in motors:
#             idle = self.settings.getMotorIdlePV(motor)
#             if idle:
#                 commands.insert(0, WaitCommand(idle, Comparison.EQUALS, 1, 0.1, 5.0))

def handle(table, lineinfo=False):
    print table
    cmds = table.createScan(lineinfo=lineinfo)
    print
    for cmd in cmds:
        print str(cmd)
    return cmds


class TableScanTest(unittest.TestCase):
    def testBasics(self):
        print "\n=== Basic Table ==="
        table_scan = TableScan(
          (   "Comment", "X ",  "Y", "Speed", "Wavelength" ),
          [
            [ "Setup",  "  1",  "2",    "30",           "" ],
            [ "Count",     "",   "",      "",        "100" ],
            [ "Wait",      "",   "",      "",        "200" ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Comment('Setup'), Set('X', 1.0), Set('Y', 2.0), Set('Speed', 30.0), Comment('Count'), Set('Wavelength', 100.0), Comment('Wait'), Set('Wavelength', 200.0)]")

        cmds = handle(table_scan, lineinfo=True)
        self.assertEqual(str(cmds), "[Comment('# Line 1'), Comment('Setup'), Set('X', 1.0), Set('Y', 2.0), Set('Speed', 30.0), Comment('# Line 2'), Comment('Count'), Set('Wavelength', 100.0), Comment('# Line 3'), Comment('Wait'), Set('Wavelength', 200.0), Comment('# End')]")

        print "\n=== Wait for time ==="
        # Also using numbers instead of strings
        table_scan = TableScan(
          (   "X",  "Y", "Wait For", "Value" ),
          [
            [  1,   2,  "seconds",   10 ],
            [  3,   4,  "seconds",   20 ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 1.0), Set('Y', 2.0), Delay(10), Log('X', 'Y'), Set('X', 3.0), Set('Y', 4.0), Delay(20), Log('X', 'Y')]")


        print "\n=== Wait for PV ==="
        table_scan = TableScan(
          (   "X",  "Y", "Wait For", "Value" ),
          [
            [ "1",  "2", "Counter1", "10" ],
            [ "3",  "4", "Counter1", "20" ],
          ]
        )
        cmds = handle(table_scan)
        #self.assertEqual(str(cmds), "")


        print "\n=== Wait for PV using 'increment' ==="
        table_scan = TableScan(
          (   "X",  "Y", "Wait For",        "Value" ),
          [
            [ "1",  "2", "Counter1",        "10" ],
            [ "3",  "4", "InfiniteCounter", "20" ],
          ]
        )
        cmds = handle(table_scan)
        #self.assertEqual(str(cmds), "")


        print "\n=== Wait for PV or Max Time ==="
        table_scan = TableScan(
          (   "X",  "Y", "Wait For", "Value", "Or Time" ),
          [
            [ "1",  "2", "Counter1", "10",    "60" ],
            [ "3",  "4", "Counter1", "20",    "00:01:00" ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 1.0), Set('Y', 2.0), Wait('Counter1', 10.0, comparison='>=', tolerance=0.1, timeout=60, errhandler='OnErrorContinue'), Log('X', 'Y', 'Counter1'), Set('X', 3.0), Set('Y', 4.0), Wait('Counter1', 20.0, comparison='>=', tolerance=0.1, timeout=60, errhandler='OnErrorContinue'), Log('X', 'Y', 'Counter1')]")


    def testStartStop(self):
        print "\n=== Start/stop at each step ==="
        table_scan = TableScan(
          (   "X",  "Y", "Wait For", "Value" ),
          [
            [ "1",  "2", "counter", "10" ],
            [ "3",  "4", "counter", "10" ],
          ],
          pre = Set('shutter', 1),
          post = Set('shutter', 0),
          start = [ Set('counter:reset', 1, completion=True),
                    Set('counter:enable', 1, completion=True),
                    Set('daq:enable', 1, completion=True)
                  ],
          stop  = [ Set('daq:enable', 0, completion=True),
                    Set('counter:enable', 0, completion=True)
                  ],
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('shutter', 1), Set('X', 1.0), Set('Y', 2.0), Set('counter:reset', 1, completion=True), Set('counter:enable', 1, completion=True), Set('daq:enable', 1, completion=True), Wait('counter', 10.0, comparison='>=', tolerance=0.1), Log('X', 'Y', 'counter'), Set('daq:enable', 0, completion=True), Set('counter:enable', 0, completion=True), Set('X', 3.0), Set('Y', 4.0), Set('counter:reset', 1, completion=True), Set('counter:enable', 1, completion=True), Set('daq:enable', 1, completion=True), Wait('counter', 10.0, comparison='>=', tolerance=0.1), Log('X', 'Y', 'counter'), Set('daq:enable', 0, completion=True), Set('counter:enable', 0, completion=True), Set('shutter', 0)]")


    def testScanSettings(self):
        print "\n=== ScanSettings configure Motor for completion and RBV ==="
        table_scan = TableScan(
          (   "X ",  "Motor1" ),
          [
            [ "  1",  "2" ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 1.0), Set('Motor1', 2.0, completion=True, readback='Motor1.RBV', timeout=100)]")


        print "\n=== Override ScanSettings for Motor ==="
        table_scan = TableScan(
          (   "Motor1",  "-cr Motor2" ),
          [
            [ "  1",  "2" ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('Motor1', 1.0, completion=True, readback='Motor1.RBV', timeout=100), Set('Motor2', 2.0)]")


    def testParallel(self):
        print "\n=== Parallel without Wait ==="
        table_scan = TableScan(
          (   "+p A", "+p B", "C", "+p D", "+p E", "F" ),
          [
            [ "1",    "2",    "3", "4",    "5",    "6" ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Parallel(Set('A', 1.0), Set('B', 2.0)), Set('C', 3.0), Parallel(Set('D', 4.0), Set('E', 5.0)), Set('F', 6.0)]")

        print "\n=== Parallel with Wait For ==="
        table_scan = TableScan(
          (   "+p A", "+p B", "C", "+p D", "+p E", "Wait For",   "Value" ),
          [
            [ "1",    "2",    "3", "4",    "5",    "completion", "10"    ],
            [ "6",    "7",    "8", "9",   "10",    "Seconds",    "10"    ],
          ],
          start = Comment('Start Run'),
          stop  = Comment('Stop Run')
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Parallel(Set('A', 1.0), Set('B', 2.0)), Set('C', 3.0), Comment('Start Run'), Parallel(Set('D', 4.0), Set('E', 5.0)), Log('A', 'B', 'C', 'D', 'E'), Comment('Stop Run'), Parallel(Set('A', 6.0), Set('B', 7.0)), Set('C', 8.0), Parallel(Set('D', 9.0), Set('E', 10.0)), Comment('Start Run'), Delay(10), Log('A', 'B', 'C', 'D', 'E'), Comment('Stop Run')]")

        print "\n=== Parallel with Delay and Wait For ==="
        table_scan = TableScan(
          (   "+p A", "+p B", "Delay",    "Wait For", "Value" ),
          [
            [ "1",    "2",    "00:05:00", "counts",   "10"    ],
          ],
          start = Comment('Start Run'),
          stop  = Comment('Stop Run'),
          special = { 'Delay': lambda cell : Delay(parseSeconds(cell)) } 
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Parallel(Set('A', 1.0), Set('B', 2.0)), Delay(300), Comment('Start Run'), Wait('counts', 10.0, comparison='>=', tolerance=0.1), Log('A', 'B', 'counts'), Comment('Stop Run')]")



    def testRange(self):
        print "\n=== Range Cells ==="
        table_scan = TableScan(
          (   " X ",  "Y", ),
          [
            [ "  1",  "", ],
            [ "   ",  "range(5)", ],
            [ "[ 0, 1]", "range(2)", ],
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 1.0), Set('Y', 0.0), Set('Y', 1.0), Set('Y', 2.0), Set('Y', 3.0), Set('Y', 4.0), Set('X', 0.0), Set('Y', 0.0), Set('X', 0.0), Set('Y', 1.0), Set('X', 1.0), Set('Y', 0.0), Set('X', 1.0), Set('Y', 1.0)]")

        table_scan = TableScan(
          (   " X ", ),
          [
            [ "range(100,200,10)", ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 100.0), Set('X', 110.0), Set('X', 120.0), Set('X', 130.0), Set('X', 140.0), Set('X', 150.0), Set('X', 160.0), Set('X', 170.0), Set('X', 180.0), Set('X', 190.0)]")

        table_scan = TableScan(
          (   " X ", ),
          [
            [ "range(175,246,70)", ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 175.0), Set('X', 245.0)]")

        print "\n=== Likely a misconfigured Range ==="
        # This used to fail by creating Set('X', 'range(175,245,70)')
        table_scan = TableScan(
          (   " X ", ),
          [
            [ "range(175,245,70)", ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 175.0)]")

        table_scan = TableScan(
          (   "X", "Y" ),
          [
            [ "range(1,0,2)", "2" ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('Y', 2.0)]")

        table_scan = TableScan(
          (   "X", "Y" ),
          [
            [ "3", "[]" ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 3.0)]")

        table_scan = TableScan(
          (   "X", "Y" ),
          [
            [ "[3]", "[2]" ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 3.0), Set('Y', 2.0)]")


        print "\n=== Fractional Range Cells ==="
        table_scan = TableScan(
          (   " X ", ),
          [
            [ "range(0.2, 5.4, 0.7)", ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 0.2), Set('X', 0.9), Set('X', 1.6), Set('X', 2.3), Set('X', 3.0), Set('X', 3.7), Set('X', 4.4), Set('X', 5.1)]")

    def testLogAlways(self):
        print "\n=== log_always ==="
        
        table_scan = TableScan(
          (   "X",  "Wait For", "Value", ),
          [
            [ "10",  "seconds",   "10" ]
          ]
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 10.0), Delay(10), Log('X')]")

        table_scan = TableScan(
          (   "X",  "Wait For", "Value", ),
          [
            [ "10",  "seconds",   "10" ]
          ],
          log_always=[ 'neutrons']
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds), "[Set('X', 10.0), Delay(10), Log('neutrons', 'X')]")

        

    def testSpecialColumns(self):
        print "\n=== Special columns ==="
        
        # Commands Start/Next/End turn into Include("lf_start.scn"), Include("lf_next.scn") resp. Include("lf_end.scn") 
        special = { 'Run Control': lambda cell : Include(cell + ".scn"),
                    'Delay':       lambda cell : Delay(parseSeconds(cell)),
                  }
        table_scan = TableScan(
          (   "Run Control", "X", "Delay",    "Wait For", "Value", ),
          [
            [ "Start",      "10", "",         "Neutrons",   "10" ],
            [ "",           "20", "00:01:00", "Neutrons",   "10" ],
            [ "Stop",       "",   "",         "",           "" ],
          ],
          special = special
        )
        cmds = handle(table_scan)
        self.assertEqual(str(cmds),
                         "[Include('Start.scn'), Set('X', 10.0), Wait('Neutrons', 10.0, comparison='>=', tolerance=0.1), Log('X', 'Neutrons'), Set('X', 20.0), Delay(60), Wait('Neutrons', 10.0, comparison='>=', tolerance=0.1), Log('X', 'Neutrons'), Include('Stop.scn')]")        


if __name__ == "__main__":
    unittest.main()
