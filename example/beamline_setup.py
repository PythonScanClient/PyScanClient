"""Example for beamline specific setup

   All scripts that access the scan server
   should start with

     'from beamline_setup import *'
"""

# Get all scan commands
from scan import *

# Replace basic Loop/Set/Wait commands with wrappers
# that utilize custom scan settings
from scan.util import SettingsBasedLoop as Loop
from scan.util import SettingsBasedSet as Set
from scan.util import SettingsBasedWait as Wait

# Each "beamline" or more generally setup that uses
# the PyScanClient should create its own ScanSettings 
class BeamlineScanSettings(ScanSettings):
    def __init__(self):
        super(BeamlineScanSettings, self).__init__()

        # Define settings based on PV name patterns
        # (regular expressions).
        # Order matters! List most generic patterns first,
        # specific PV names last.
        # For example, motors should use completion, and check a readback
        self.defineDeviceClass("motor_.", completion=True, readback=True)
        # The specific motors in the simulation.db, however, don't support completion
        self.defineDeviceClass("motor_x", completion=False, readback=False)
        self.defineDeviceClass("motor_y", completion=False, readback=False)
        self.defineDeviceClass("shutter", readback=True)
        # The simulated "setpoint" uses a different PV "readback" as its readback.
        # (readback=False skips readback check
        #  readback=True calls getReadbackName(pv) which typically returns the PV itself,
        #  readback='whatever' uses provided PV
        # )
        self.defineDeviceClass("setpoint", completion=False, readback="readback", tolerance=0.1, timeout=20)
        # When waiting for proton charge or neutron counts, use "increase by"
        self.defineDeviceClass("pcharge", comparison="increase by")
        self.defineDeviceClass("neutrons", comparison="increase by")
        
        # Each site may add more to its site-specific configuration.
        # The example/opi for alignment uses these to
        # populate drop-downs
        self.settable = [ "motor_x", "motor_y" ]
        self.waitable = [ "seconds", "time", "pcharge" ]
        self.loggable = [ "signal" ]

    def getReadbackName(self, device_name):
        # Anything that looks like a motor very likely has a .RBV.
        # But that does not apply to the simulated motor_x, motor_y
        if device_name in ( 'motor_x', 'motor_y' ):
            return device_name
        if "motor" in device_name:
           return device_name + ".RBV"

# Install beam line specific scan settings
scan_settings = BeamlineScanSettings()
setScanSettings(scan_settings)

# 'Meta Commands'
def Pre():
    return Set('shutter', 1)
def Post():
    return Set('shutter', 0)

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
    return  Sequence(Set('loc://chopper:run(0)', 0),
                     Set('loc://chopper:wlen(0)', wavelength),
                     Set('loc://chopper:phs(0)', phase),
                     Set('loc://chopper:run(0)', 1)
                    )

def table_scan(headers, rows):
    """Create table scan with pre/post/start/stop for this beam line"""
    table = TableScan(headers, rows,
                      pre=Pre(),
                      post=Post(),
                      start=Start(),
                      stop=Stop())
    return table.createScan()

# Shortcut
ndim = createNDimScan

# Create a scan client, using the host name that executes the scan server
scan_client = ScanClient('localhost')

# As a convenience, `python beamline_setup.py` prints settings
if __name__ == '__main__':
    from scan.util.scan_settings import getScanSettings

    print("Beam Line scan settings")
    print("=======================")
    for setting in getScanSettings().device_settings:
        print(setting)
    print("")
    print("Scan Client")
    print("===========")
    print(scan_client)
