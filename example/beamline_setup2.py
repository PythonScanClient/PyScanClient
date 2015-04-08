"""Example for beamline specific setup using JSON file
"""
from scan import *
from scan.util import SettingsBasedLoop as Loop
from scan.util import SettingsBasedSet as Set
from scan.util import SettingsBasedWait as Wait

# Custom scan settings
my_settings = ScanSettings()
my_settings.loadDeviceClasses("scan_local.json")

print my_settings

setScanSettings(my_settings)



import unittest

class TestScanClient(unittest.TestCase):
    def testSet(self):
        self.assertEqual(str(Set('setpoint', 1)), "Set('setpoint', 1, completion=True, readback='readback')")
        self.assertEqual(str(Set('setpoint', 1, completion=False)), "Set('setpoint', 1, readback='readback')")
        self.assertEqual(str(Set('setpoint', 1, readback=False)), "Set('setpoint', 1, completion=True)")
        self.assertEqual(str(Set('setpoint', 1, timeout=10)), "Set('setpoint', 1, completion=True, readback='readback', timeout=10)")

    def testLoop(self):
        self.assertEqual(str(Loop('x', 1, 5, 0.5)), "Loop('x', 1, 5, 0.5)")
        self.assertEqual(str(Loop('motor_x', 1, 5, 0.5)), "Loop('motor_x', 1, 5, 0.5, completion=True, readback='motor_x')")
        self.assertEqual(str(Loop('motor_x', 1, 5, 0.5, completion=False)), "Loop('motor_x', 1, 5, 0.5, readback='motor_x')")
        self.assertEqual(str(Loop('motor_x', 1, 5, 0.5, completion=False, readback=False)), "Loop('motor_x', 1, 5, 0.5)")
        self.assertEqual(str(Loop('motor_x', 1, 5, 0.5, Comment(''), completion=False, readback=False)),
                         "Loop('motor_x', 1, 5, 0.5, [ Comment('') ])")
        self.assertEqual(str(Loop('motor_x', 1, 5, 0.5, Comment('a'), Comment('b'), completion=False, readback=False)),
                         "Loop('motor_x', 1, 5, 0.5, [ Comment('a'), Comment('b') ])")
        self.assertEqual(str(Loop('motor_x', 1, 5, 0.5, [ Comment('a'), Comment('b') ], completion=False, readback=False)),
                         "Loop('motor_x', 1, 5, 0.5, [ Comment('a'), Comment('b') ])")
        
    def testWait(self):
        self.assertEqual(str(Wait('whatever', 1)), "Wait('whatever', 1, comparison='>=')")
        self.assertEqual(str(Wait('pcharge', 1)), "Wait('pcharge', 1, comparison='increase by')")
        self.assertEqual(str(Wait('pcharge', 1, timeout=5)), "Wait('pcharge', 1, comparison='increase by', timeout=5)")
        self.assertEqual(str(Wait('pcharge', 1, timeout=5, comparison='>=')), "Wait('pcharge', 1, comparison='>=', timeout=5)")


if __name__ == '__main__':
    unittest.main()
