from scan.util.scan_settings import ScanSettings

class MyScanSettings(ScanSettings):
    """Example for site-specific scan settings.
       
       When installing the python scan client at a site,
       you need to make such a site-specific version
       avaialble to all users who write python scripts.
       """
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
        
        # When waiting for this counter, use 'to increase by' instead of '='
        self.defineDeviceClass("PerpetualCounter", comparison='to increase by')
        
    def getReadbackName(self, device_name):
        # Motors use their *.RBV field for readback
        if device_name.startswith("pos"):
            return device_name + ".RBV"
        return device_name
