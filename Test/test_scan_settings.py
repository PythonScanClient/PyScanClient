"""
Unit test of ScanSettings

@author: Kay Kasemir
"""
import unittest
from scan.util.scan_settings import DeviceSettings, ScanSettings

class DeviceSettingsTest(unittest.TestCase):
    def testDeviceSettings(self):
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

    def testBasicScanSettings(self):
        settings = ScanSettings()
        
        # Define special settings for some devices
        settings.defineDeviceClass("My:Lakeshore.*", completion=True, readback=False, timeout=300)
        
        # Check device that should have special settings
        s = settings.getDeviceSettings("My:Lakeshore1")
        print s
        self.assertEquals(s.getName(), "My:Lakeshore1")
        self.assertEquals(s.getCompletion(), True)
        self.assertEquals(s.getReadback(), None)
        self.assertEquals(s.getTimeout(), 300)

        # Check device that should NOT have them
        s = settings.getDeviceSettings("Your:Lakeshore1")
        print s
        self.assertEquals(s.getName(), "Your:Lakeshore1")
        self.assertEquals(s.getCompletion(), False)
        self.assertEquals(s.getReadback(), "Your:Lakeshore1")


 
if __name__ == "__main__":
    unittest.main()
    settings = ScanSettings()

    print settings.parseDeviceModifiers("plain_device")
    print settings.parseDeviceModifiers("-r no_readback")
    print settings.parseDeviceModifiers("+r with_readback")
    print settings.parseDeviceModifiers("+c with_callback")
    print settings.parseDeviceModifiers("+cr with_callback_and_readback")
    print settings.parseDeviceModifiers("+rc with_callback_and_readback")
    print settings.parseDeviceModifiers("+c +r with_callback_and_readback")
    print settings.parseDeviceModifiers("+c+r with_callback_and_readback")
    print settings.parseDeviceModifiers("+c +rp with_callback_and_readback_in_parallel")
    print settings.parseDeviceModifiers("+p with:Mot:callback_and_readback_in_parallel")


    print settings.parseDeviceModifiers("Other")
    print settings.parseDevice("Other")

    
    print "%-22s: %-20s %-35s %-10s %-10s %-10s" % ( "Device", "PV", "Readback", "Completion?", "Timeout", "Tolerance" )
    print "---------------------------------------------------------------------------------------------------------------"

    
    print "Title PV: %s" % settings.title
    
    settings.device_settings['TestWithCallback'] = { 'callback': True, 'readback': 'Test', 'timeout': None }
    settings.device_settings['TestWithoutReadback'] = { 'callback': False, 'readback': None, 'timeout': None }
    for device in [ "BL99:Mot:Whatever", "Speed",
                    "-r-c BL99:Mot:Whatever",
                    "-c-r BL99:Mot:Whatever",
                    "BL99:Other", "+c BL99:Other", "-r BL99:Other", "-r+r BL99:Other",
                    "TestWithCallback", "TestWithoutReadback"
                  ]:
                    
        (pv, readback, completion, timeout, tolerance) = settings.parseDevice(device)
        if readback is None:
            readback = "-None-"
        print "%-22s: %-20s %-35s %-10s %-10s %-10s" % (device, pv, readback, completion, timeout, tolerance)

