"""
Unit test of ScanSettings

@author: Kay Kasemir
"""
from __future__ import print_function
import unittest
from scan.commands.delay import Delay
from scan.util.scan_settings import DeviceSettings, ScanSettings, setScanSettings, SettingsBasedSet, SettingsBasedLoop, SettingsBasedWait

class MyScanSettings(ScanSettings):
    def __init__(self):
        super(MyScanSettings, self).__init__()
        # Settings are added in the order of 'most generic first'.
        # By default, always use readback:
        self.defineDeviceClass(".*", readback=True)
        
        # Define special settings for some devices
        # Temperature controller uses completion, but no readback
        self.defineDeviceClass("My:Lakeshore.*", completion=True, readback=False, timeout=300, tolerance=10)
        # Motor uses completion and readback (with special readback name, see below)
        self.defineDeviceClass("My:Motor.*", completion=True, readback=True, timeout=100)
        # Counter comared by increment, not absolute value
        self.defineDeviceClass("PerpetualCounter", comparison='increase by')
        
    def getReadbackName(self, device_name):
        # Motors use their *.RBV field for readback
        if "Motor" in device_name:
            return device_name + ".RBV"
        return device_name


class DeviceSettingsTest(unittest.TestCase):
    def testDefaultSettings(self):
        s = DeviceSettings("device", readback=False)
        print(s)
        self.assertEquals(s.getName(), "device")
        self.assertEquals(s.getReadback(), None)

        s = DeviceSettings("device", readback=True)
        print(s)
        self.assertEquals(s.getName(), "device")
        self.assertEquals(s.getReadback(), "device")

        s = DeviceSettings("device", readback="other")
        print(s)
        self.assertEquals(s.getName(), "device")
        self.assertEquals(s.getReadback(), "other")

    def testCustomSettings(self):
        settings = MyScanSettings()
        
        # Device that has no specific settings, using the default
        s = settings.getDefaultSettings("SomeRandomDevice")
        print(s)
        self.assertEquals(s.getName(), "SomeRandomDevice")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "SomeRandomDevice")
        self.assertEquals(s.getTimeout(), 0)
        self.assertTrue(s.getTolerance() is None)
        
        # Check device that should have special settings
        s = settings.getDefaultSettings("My:Lakeshore1")
        print(s)
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(s.getTimeout(), 300)
        self.assertEquals(s.getTolerance(), 10)

        # Check device that should NOT have them
        s = settings.getDefaultSettings("Your:Lakeshore1")
        print(s)
        self.assertEquals(s.getName(), "Your:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "Your:Lakeshore1")
        
        # 'Motor' that uses *.RBV for a readback
        s = settings.getDefaultSettings("My:Motor:47")
        print(s)
        self.assertEquals(s.getName(), "My:Motor:47")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), "My:Motor:47.RBV")
        self.assertEquals(s.getTimeout(), 100)
        self.assertTrue(s.getTolerance() is None)

        # Different comparisons
        s = settings.getDefaultSettings("SomeCounter")
        print(s)
        self.assertEquals(s.getComparison(), '>=')

        s = settings.getDefaultSettings("PerpetualCounter")
        print(s)
        self.assertEquals(s.getComparison(), 'increase by')


    def testDeviceModifiers(self):
        settings = MyScanSettings()
        
        spec = "My:Lakeshore1"
        s = settings.parseDeviceSettings(spec)
        print("%s -> %s" % (spec, s))
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(s.getTimeout(), 300)
        self.assertEquals(s.getParallel(), False)

        spec = "+p My:Lakeshore1"
        s = settings.parseDeviceSettings(spec)
        self.assertEquals(s.getParallel(), True)

        spec = "-c My:Lakeshore1"
        s = settings.parseDeviceSettings(spec)
        print("%s -> %s" % (spec, s))
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), None)

        spec = "+p-c+r My:Lakeshore1"
        s = settings.parseDeviceSettings(spec)
        print("%s -> %s" % (spec, s))
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "My:Lakeshore1")
        self.assertEquals(s.getParallel(), True)

        spec = "+pr My:Lakeshore1"
        s = settings.parseDeviceSettings(spec)
        print("%s -> %s" % (spec, s))
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getReadback(), "My:Lakeshore1")
        self.assertEquals(s.getParallel(), True)

        spec = "+p-cr My:Motor:47"
        s = settings.parseDeviceSettings(spec)
        print("%s -> %s" % (spec, s))
        self.assertEquals(s.getName(), "My:Motor:47")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(s.getParallel(), True)


    def testSettingsBasedSet(self):
        setScanSettings(MyScanSettings())

        cmd = SettingsBasedSet('My:Motor1', 42)
        self.assertEquals(str(cmd), "Set('My:Motor1', 42, completion=True, timeout=100, readback='My:Motor1.RBV', tolerance=0.100000)")

        cmd = SettingsBasedSet('Unknown:Motor1', 42)
        self.assertEquals(str(cmd), "Set('Unknown:Motor1', 42, readback='Unknown:Motor1.RBV', tolerance=0.100000)")

        cmd = SettingsBasedSet('Unknown:Motor1', 42, readback=False)
        self.assertEquals(str(cmd), "Set('Unknown:Motor1', 42)")


    def testSettingsBasedLoop(self):
        setScanSettings(MyScanSettings())

        cmd = SettingsBasedLoop('My:Motor1', 1, 10, 2, Delay(1)); 
        self.assertEquals(str(cmd), "Loop('My:Motor1', 1, 10, 2, [ Delay(1) ], completion=True, readback='My:Motor1.RBV', tolerance=0.2, timeout=100)")

        cmd = SettingsBasedLoop('My:Motor1', 1, 10, 2, Delay(1), Delay(2)); 
        self.assertEquals(str(cmd), "Loop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], completion=True, readback='My:Motor1.RBV', tolerance=0.2, timeout=100)")

        cmd = SettingsBasedLoop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ]); 
        self.assertEquals(str(cmd), "Loop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], completion=True, readback='My:Motor1.RBV', tolerance=0.2, timeout=100)")

        cmd = SettingsBasedLoop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], completion=False); 
        self.assertEquals(str(cmd), "Loop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], readback='My:Motor1.RBV', tolerance=0.2, timeout=100)")

        cmd = SettingsBasedLoop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], completion=False, timeout=0); 
        self.assertEquals(str(cmd), "Loop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], readback='My:Motor1.RBV', tolerance=0.2)")

        cmd = SettingsBasedLoop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ], completion=False, readback=False); 
        self.assertEquals(str(cmd), "Loop('My:Motor1', 1, 10, 2, [ Delay(1), Delay(2) ])")




    def testSettingsBasedWait(self):
        setScanSettings(MyScanSettings())

        cmd = SettingsBasedWait('SomePV', 42)
        self.assertEquals(str(cmd), "Wait('SomePV', 42, comparison='>=', tolerance=0.1)")

        cmd = SettingsBasedWait('PerpetualCounter', 42)
        self.assertEquals(str(cmd), "Wait('PerpetualCounter', 42, comparison='increase by', tolerance=0.1)")



if __name__ == "__main__":
    unittest.main()
    
