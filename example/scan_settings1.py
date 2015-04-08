from scan.util.scan_settings import ScanSettings, setScanSettings

# Note how we replace the original Set() and Wait() commands with those that utilize ScanSettings
from scan.util.scan_settings import SettingsBasedSet as Set
from scan.util.scan_settings import SettingsBasedWait as Wait

class MyScanSettings(ScanSettings):
    """Example for site-specific scan settings."""
    def __init__(self):
        super(MyScanSettings, self).__init__()

        # Define special settings for some devices
        # based on regular expressions for the PV names
        
        # All temperature controllers use completion, but there's no readback to check
        self.defineDeviceClass(".*temp.*", completion=True, readback=False, timeout=300)

        # Special device with dedicated reachback PV
        self.defineDeviceClass("MyXYZDevice:setpoint", readback="MyXYZDevice:readback",
                               timeout=10, tolerance=0.5)

        # Motors should use completion, and readback.
        # Name of readback is based on motor name, see getReadbackName()
        self.defineDeviceClass("pos.*", completion=True, readback=True, timeout=100)
        
        # When waiting for this counter, use 'increase by' instead of '='
        self.defineDeviceClass("PerpetualCounter", comparison='increase by')
        
    def getReadbackName(self, device_name):
        # Motors use their *.RBV field for readback
        if device_name.startswith("pos"):
            return device_name + ".RBV"
        return device_name

if __name__ == "__main__":
    print "Without scan settings:"
    cmds = [
            Set('temperature', 10),
            Wait('PerpetualCounter', 10),
           ]
    for cmd in cmds:
        print cmd
    # Result:
    # Set('temperature', 10)
    # Wait('PerpetualCounter', 10, comparison='>=')
      
    setScanSettings(MyScanSettings())
    
    print "With scan settings:"
    cmds = [
            Set('temperature', 10),
            Wait('PerpetualCounter', 10),
           ]
    for cmd in cmds:
        print cmd
    # Result:    
    # Set('temperature', 10, completion=True, timeOut=300)
    # Wait('PerpetualCounter', 10, comparison='increase by')