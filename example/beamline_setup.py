"""Example for beamline specific setup"""

from scan import *
from scan.commands.set import Set as OriginalSet

# Custom scan settings
class BeamlineScanSettings(ScanSettings):
    def __init__(self):
        super(BeamlineScanSettings, self).__init__()
        # Define several PVs to use completion etc.
        self.defineDeviceClass("chopper:.*", completion=True)
        self.defineDeviceClass("daq", completion=True)
        self.defineDeviceClass(".*:reset", completion=True)
        self.defineDeviceClass(".pos", completion=True, readback=True)

    def getReadbackName(self, device_name):
        # Anything ending in 'pos' is a motor with custom readback PV
        if device_name.endswith("pos"):
            return device_name + ".RBV"
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

# 'Meta Commands'
def Start():
    return Sequence(scan_settings.Set('counters:reset', 1),
                    scan_settings.Set('daq', 1) )

def Stop():
    return scan_settings.Set('daq', 0)

def TakeData(counter, limit):
    return  Sequence(Start(), Wait(counter, limit), Stop())

def SetChopper(wavelength, phase):
    return  Sequence(scan_settings.Set('chopper:run', 0),
                     scan_settings.Set('chopper:wlen', wavelength),
                     scan_settings.Set('chopper:phs', phase),
                     scan_settings.Set('chopper:run', 1)
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

