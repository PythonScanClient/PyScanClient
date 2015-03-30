"""
Unit test of ScanSettings

@author: Kay Kasemir
"""
import unittest
from scan.util.scan_settings import DeviceSettings, ScanSettings

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
        self.defineDeviceClass("PerpetualCounter", comparison='to increase by')
        
    def getReadbackName(self, device_name):
        # Motors use their *.RBV field for readback
        if "Motor" in device_name:
            return device_name + ".RBV"
        return device_name


class DeviceSettingsTest(unittest.TestCase):
    def testDefaultSettings(self):
        s = DeviceSettings("device", readback=False)
        print s
        self.assertEquals(s.getName(), "device")
        self.assertEquals(s.getReadback(), None)

        s = DeviceSettings("device", readback=True)
        print s
        self.assertEquals(s.getName(), "device")
        self.assertEquals(s.getReadback(), "device")

        s = DeviceSettings("device", readback="other")
        print s
        self.assertEquals(s.getName(), "device")
        self.assertEquals(s.getReadback(), "other")

    def testCustomSettings(self):
        settings = MyScanSettings()
        
        # Device that has no specific settings, using the default
        s = settings.getDefaultSettings("SomeRandomDevice")
        print s
        self.assertEquals(s.getName(), "SomeRandomDevice")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "SomeRandomDevice")
        self.assertEquals(s.getTimeout(), 0)
        self.assertEquals(s.getTolerance(), 0)
        
        # Check device that should have special settings
        s = settings.getDefaultSettings("My:Lakeshore1")
        print s
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(s.getTimeout(), 300)
        self.assertEquals(s.getTolerance(), 10)

        # Check device that should NOT have them
        s = settings.getDefaultSettings("Your:Lakeshore1")
        print s
        self.assertEquals(s.getName(), "Your:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "Your:Lakeshore1")
        
        # 'Motor' that uses *.RBV for a readback
        s = settings.getDefaultSettings("My:Motor:47")
        print s
        self.assertEquals(s.getName(), "My:Motor:47")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), "My:Motor:47.RBV")
        self.assertEquals(s.getTimeout(), 100)
        self.assertEquals(s.getTolerance(), 0)

        # Different comparisons
        s = settings.getDefaultSettings("SomeCounter")
        print s
        self.assertEquals(s.getComparison(), '>=')

        s = settings.getDefaultSettings("PerpetualCounter")
        print s
        self.assertEquals(s.getComparison(), 'to increase by')


    def testDeviceModifiers(self):
        settings = MyScanSettings()
        
        spec = "My:Lakeshore1"
        (s, p) = settings.parseDeviceSettings(spec)
        print "%s -> %s" % (spec, s)
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(s.getTimeout(), 300)
        self.assertEquals(p, False)

        spec = "+p My:Lakeshore1"
        (s, p) = settings.parseDeviceSettings(spec)
        self.assertEquals(p, True)

        spec = "-c My:Lakeshore1"
        (s, p) = settings.parseDeviceSettings(spec)
        print "%s -> %s" % (spec, s)
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), None)

        spec = "+p-c+r My:Lakeshore1"
        (s, p) = settings.parseDeviceSettings(spec)
        print "%s -> %s" % (spec, s)
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "My:Lakeshore1")
        self.assertEquals(p, True)

        spec = "+pr My:Lakeshore1"
        (s, p) = settings.parseDeviceSettings(spec)
        print "%s -> %s" % (spec, s)
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getReadback(), "My:Lakeshore1")
        self.assertEquals(p, True)

        spec = "+p-cr My:Motor:47"
        (s, p) = settings.parseDeviceSettings(spec)
        print "%s -> %s" % (spec, s)
        self.assertEquals(s.getName(), "My:Motor:47")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(p, True)


if __name__ == "__main__":
    unittest.main()
    