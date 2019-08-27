"""Unit test of the AlignmentScan

   @author: Kay Kasemir
"""
from __future__ import print_function
import unittest
from scan.commands import Set, CommandSequence
from scan.alignment import AlignmentScan


class AlignmentTest(unittest.TestCase):
    def testBasics(self):
        align = AlignmentScan("motor_x", 0, 10, 0.5, "seconds", 0.5, "signal",
                              pre=Set("motor_y", 3),
                              find_command="FindPeak")
        cmds = align.createScan()
        print(CommandSequence(cmds))
        
        self.assertEqual(str(cmds), "[Set('Demo:CS:Scan:Fit:Height', 0), Set('motor_y', 3), Loop('motor_x', 0, 10, 0.5, [ Delay(0.5), Log('signal', 'motor_x'), Script('WriteDataToPV', 'motor_x', 'Demo:CS:Scan:Fit:Data:X'), Script('WriteDataToPV', 'signal', 'Demo:CS:Scan:Fit:Data:Y', '-', '1') ]), Script('FindPeak', 'motor_x', 'signal', '-', '1', 'Demo:CS:Scan:Fit:Pos', 'Demo:CS:Scan:Fit:Height', 'Demo:CS:Scan:Fit:Width')]")


if __name__ == "__main__":
    unittest.main()