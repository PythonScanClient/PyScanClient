"""Example for beamline specific setup

Uses the scan server example database
plus some local PVs to fake devices.
"""

from scan import *
from symbol import comparison

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
        # Prime example would be a motor, but not in this example..
#         if "motor" in device_name:
#             return device_name + ".RBV"
        return device_name

scan_settings = BeamlineScanSettings()


# Redefine plain commands to use the scan settings
def Set(device, value, **kvargs):
    """Set a device to a value.
    
    With optional check of completion and readback verification.
    
    :param device:     Device name
    :param value:      Value
    
    Uses beam line specific defaults, but may override the following:

    :param completion: Await callback completion?
    :param readback:   `False` to not check any readback,
                       `True` to wait for readback from the `device`,
                       or name of specific device to check for readback.
    :param tolerance:  Tolerance when checking numeric `readback`.
    :param timeout:    Timeout in seconds, used for `completion` and `readback`.
    
    Example:
        >>> cmd = Set('position', 10.5)
        
    """
    cmd = scan_settings.Set(device, value)
    if 'completion' in kvargs:
        cmd.setCompletion(kvargs['completion'])
    if 'readback' in kvargs:
        cmd.setReadback(kvargs['readback'])
    if 'tolerance' in kvargs:
        cmd.setTolerance(kvargs['tolerance'])
    if 'timeout' in kvargs:
        cmd.setTimeout(kvargs['timeout'])
    return cmd

def Wait(device, value, **kvargs):
    """Wait until a condition is met, i.e. a device reaches a value.
    
    :param  device:      Name of PV or device.
    :param  value:       Desired value.

    Uses beam line specific defaults, but may override the following:

    :param  comparison:  How current value is compared to the desired value.
                         Defaults to '='.
                         Other options: '>', '>=', '<' , '<=', 'increase by','decrease by'
    :param  tolerance:  Tolerance used for numeric comparison. Defaults to 0, not used for string values.
    :param  timeout:    Timeout in seconds. Default 0 to wait 'forever'.
        
    Example:
        >>> cmd = Wait('shutter', 1)
    """
    cmd = scan_settings.Wait(device, value)
    if 'comparison' in kvargs:
        cmd.setComparison(kvargs['comparison'])
    if 'tolerance' in kvargs:
        cmd.setTolerance(kvargs['tolerance'])
    if 'timeout' in kvargs:
        cmd.setTimeout(kvargs['timeout'])
    return cmd

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


class BeamlineScanClient(ScanClient):
    """Scan Client for beam line"""
    def __init__(self):
        super(BeamlineScanClient, self).__init__('localhost')

    def ls(self):
        """List all scans on the server"""
        for scan in self.scanInfos():
            print scan

    def ndim(self, *args):
        """Create N-Dimensional scan
           with scan settings for this beam line
        """
        return CommandSequence(createNDimScan(scan_settings, *args))
    
    def table(self, headers, rows):
        """Create table scan
           with scan settings and pre/post/start/stop
           for this beam line
        """
        table = TableScan(scan_settings, headers, rows,
                          start=Start(),
                          stop=Stop())
        return CommandSequence(table.createScan())

scan = BeamlineScanClient()





import unittest

class TestScanClient(unittest.TestCase):
    def testSet(self):
        self.assertEqual(str(Set('setpoint', 1)), "Set('setpoint', 1, completion=True, readback='readback')")
        self.assertEqual(str(Set('setpoint', 1, completion=False)), "Set('setpoint', 1, readback='readback')")
        self.assertEqual(str(Set('setpoint', 1, readback=False)), "Set('setpoint', 1, completion=True)")
        self.assertEqual(str(Set('setpoint', 1, timeout=10)), "Set('setpoint', 1, completion=True, readback='readback', timeout=10)")

    def testWait(self):
        self.assertEqual(str(Wait('whatever', 1)), "Wait('whatever', 1, comparison='>=')")
        self.assertEqual(str(Wait('pcharge', 1)), "Wait('pcharge', 1, comparison='increase by')")
        self.assertEqual(str(Wait('pcharge', 1, timeout=5)), "Wait('pcharge', 1, comparison='increase by', timeout=5)")
        self.assertEqual(str(Wait('pcharge', 1, timeout=5, comparison='>=')), "Wait('pcharge', 1, comparison='>=', timeout=5)")


if __name__ == '__main__':
    unittest.main()
