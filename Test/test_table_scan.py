"""Unit test of the TableScan

   @author: Kay Kasemir
"""
import unittest
from scan.table import TableScan

class TableScanTest(unittest.TestCase):
    def testXML(self):
        settings = None
        
        print "\n=== Basic Table ==="
        table_scan = TableScan(settings,
          (   "Comment", "X ",  "Y", "Speed", "Wavelength" ),
          [
            [ "Setup",  "  1",  "2",    "30",           "" ],
            [ "Count",     "",   "",      "",        "100" ],
            [ "Wait",      "",   "",      "",        "200" ],
          ]
        )
        print table_scan
        cmds = table_scan.createScan()
        print "\nScan:"
        for cmd in cmds:
            print str(cmd)
        
        # TODO Check result
        #self.assertEqual(str(cmds), "[Comment 'Setup', Set 'X' = 1.0, Set 'Y' = 2.0, Set 'Speed' = 30.0, Comment 'Count', Set 'Wavelength' = 100.0, Comment 'Wait', Set 'Wavelength' = 200.0]")


        print "\n=== Range Cells ==="
        table_scan = TableScan(settings,
          (   " X ",  "Y", ),
          [
            [ "  1",  "", ],
            [ "   ",  "range(5)", ],
            [ "[ 0, 1]", "range(2)", ],
          ]
        )
        print table_scan
        cmds = table_scan.createScan()
        print "\nScan:"
        for cmd in cmds:
            print str(cmd)
        
        # TODO Check result
        #self.assertEqual(str(cmds), "[Set 'X' = 1.0, Set 'Y' = 0.0, Set 'Y' = 1.0, Set 'Y' = 2.0, Set 'Y' = 3.0, Set 'Y' = 4.0, Set 'X' = 0.0, Set 'Y' = 0.0, Set 'X' = 0.0, Set 'Y' = 1.0, Set 'X' = 1.0, Set 'Y' = 0.0, Set 'X' = 1.0, Set 'Y' = 1.0]")



if __name__ == "__main__":
    unittest.main()