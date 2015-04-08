"""Example for beamline specific setup

Uses the scan server example database
plus some local PVs to fake devices.
"""

from scan import *

# Note that the basic Loop/Set/Wait commands are replaced by
# those that utilize custom scan settings
from scan.util import SettingsBasedLoop as Loop
from scan.util import SettingsBasedSet as Set
from scan.util import SettingsBasedWait as Wait

# Custom scan settings
class BeamlineScanSettings(ScanSettings):
    def __init__(self):
        super(BeamlineScanSettings, self).__init__()
        # Define several PVs to use completion etc.
        self.defineDeviceClass("shutter", readback=True)
        self.defineDeviceClass("chopper:.*", completion=True)
        self.defineDeviceClass(".*daq.*", completion=True)
        self.defineDeviceClass("motor_.", completion=True, readback=True)
        self.defineDeviceClass("setpoint", completion=True, readback="readback", tolerance=0.1)
        self.defineDeviceClass("pcharge", comparison="increase by")
        self.defineDeviceClass("neutrons", comparison="increase by")

    def getReadbackName(self, device_name):
        # Prime example would be a motor:
        #if "motor" in device_name:
        #    return device_name + ".RBV"
        return device_name

# Install beam line specific scan settings
setScanSettings(BeamlineScanSettings())


# 'Meta Commands'
def Start():
    """Start data acquisition"""
    return Sequence( Set('loc://daq_reset(0)', 1),
                     Set('loc://daq(0)', 1)
                   )

def Stop():
    """Stop data acquisition"""
    return Set('loc://daq(0)', 0)

def TakeData(counter, limit):
    return  Sequence(Start(), Wait(counter, limit), Stop())

def SetChopper(wavelength, phase):
    return  Sequence(scan_settings.Set('loc://chopper:run(0)', 0),
                     scan_settings.Set('loc://chopper:wlen(0)', wavelength),
                     scan_settings.Set('loc://chopper:phs(0)', phase),
                     scan_settings.Set('loc://chopper:run(0)', 1)
                    )


def table_scan(headers, rows):
    """Create table scan with pre/post/start/stop for this beam line"""
    table = TableScan(headers, rows,
                      start=Start(),
                      stop=Stop())
    return table.createScan()

# Shortcut
ndim = createNDimScan

# Create a scan client, using the host name that executes the scan server
scan_client = ScanClient('localhost')





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
