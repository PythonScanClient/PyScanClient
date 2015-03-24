"""
Scan settings

ScanSettings class is meant to be the basis
of a site-specific implementation.

@author: Kay Kasemir
"""
import re

class DeviceSettings(object):
    """Settings for a device, how it should be accessed in a scan.
    
       With completion?
       With readback? If yes, using what device name?
       With callback?
       ...
    """
    def __init__(self, name, completion=False, readback=False, timeout=0.0, tolerance=0.0, comparison='>='):
        """name:       Device name
           completion: True to use completion
           readback:   False to not use a readback,
                       True to use the primary name,
                       Actual read back name if different from the promary device name. 
           timeout:    Time out for callback and readback in seconds. 0 to wait forever.
           tolerance:  Tolerance for numeric readback comparison.
           comparison: Comparison to use in Wait commands
        """
        self.name = name
        self.completion = completion
        self.readback = readback
        self.timeout = timeout
        self.tolerance = tolerance
        self.comparison = comparison
    
    def getName(self):
        """Returns device name."""
        return self.name

    def getCompletion(self):
        """Returns True when device should be accessed with completion."""
        return self.completion

    def getReadback(self):
        """Get device name to use for readback, or None."""
        if not self.readback:
            return None
        return self.name if self.readback == True else self.readback

    def getTimeout(self):
        """Returns timeout in seconds."""
        return self.timeout
    
    def getTolerance(self):
        """Returns tolerance for numeric readback check."""
        return self.tolerance

    def getComparison(self):
        """Returns comparison for Wait command."""
        return self.comparison
    
    def __repr__(self):
        rb = self.getReadback()
        if rb:
            rb = "'" + rb + "'"
        return "DeviceSettings('%s', completion=%s, readback=%s, timeout=%g, tolerance=%g, comparison='%s')" % (
                self.name, str(self.completion), rb,  self.timeout, self.tolerance, self.comparison)



class ScanSettings(object):
    """Scan Settings
    
       Site-specific implementation is derived from the ScanSettings class.
       In its constructor, derived classes can call defineDeviceClass() to
       define settings for devices that match a certain name.
       
       In addition, derived class may override computeReadbackName() to
       provide for example the *.RBV for a motor PV.
    """

    def __init__(self):
        """Derived class can override constructor
           to add calls to defineDeviceClass()
        """
        # List that holds DeviceSettings, but NOT exactly as it's passed out to
        # uses of this class:
        # The device_settings[].name is a regular expression pattern for device names.
        self.device_settings = list()
        
        # In derived class, may register special behavior for certain devices
        # self.defineDeviceClass("My:Motor.*", completion=True, readback=True, timeout=100)

    def getReadbackName(self, device_name):
        """device_name: Primary device name
           Returns the corresponding device name for readback check
           
           Derived class may override to compute the readback name
        """
        
        # Example for derived class:
        #if "Motor" in device_name:
        #    return device_name + ".RBV"
        
        return device_name
        
    def defineDeviceClass(self, name_pattern, completion=False, readback=False, timeout=0.0, tolerance=0.0, comparison='>='):
        """name_pattern: Device name pattern (regular expression)
           completion:   True to use completion
           readback:     False to not use a readback,
                         True to use the primary name,
                         Actual read back name if different from the promary device name. 
           timeout:      Time out for callback and readback in seconds. 0 to wait forever.
           tolerance:    Tolerance for numeric readback comparison.
           comparison:   Comparison to use in Wait commands.
        """
        self.device_settings.append(DeviceSettings(name_pattern, completion, readback, timeout, tolerance, comparison))                
                        
    def getDefaultSettings(self, name):
        """name: Name of device
           Returns suggested DeviceSettings for that device.
        """
        for setting in self.device_settings:
            if re.match(setting.getName(), name):
                # rb = False (no readback), True (use device name), or "SomeExactName" 
                rb = setting.readback
                if rb == True:
                    rb = self.getReadbackName(name)
                return DeviceSettings(name, setting.getCompletion(), rb, setting.getTimeout(), setting.getTolerance(), setting.getComparison())
        return DeviceSettings(name)
    
    def parseDeviceSettings(self, prefixed_device):
        """Parse a device name that may be prefixed with modifiers
           that override the default settings for the device.
           
           Supported modifiers:
           -c: Do not await completion
           +c: Do await completion
           -r: Do not check readback
           +r: Do check readback
           +p: Access in parallel
        
           @return: ( DeviceSettings(name), parallel )
        """
        mod_device = prefixed_device.strip()
        readback = None
        completion = None
        parallel = False
        
        while mod_device.startswith('+') or mod_device.startswith('-'):
            yesno = mod_device.startswith('+')
            mod_device = mod_device[1:]
            # one or more modifiers may follow the +|-
            while not mod_device[0] in " +-":
                if mod_device[0] == 'r':
                    readback = yesno
                elif mod_device[0] == 'c':
                    completion = yesno
                elif mod_device[0] == 'p':
                    parallel = yesno
                else:
                    raise Exception("Unknown device modifier %s in %s" % (mod_device[0], prefixed_device))
                mod_device = mod_device[1:]
            mod_device = mod_device.strip()
       
        device = mod_device

        default = self.getDefaultSettings(device)

        # Use defaults unless modifiers were provided
        if default.getReadback()  and readback is None:
            readback = default.getReadback()
        if completion is None:
            completion = default.getCompletion()

        # Turn "do use readback" into the device to use,
        # (def_readback would already provide the device)           
        if readback == True:
            readback = device
        
        return ( DeviceSettings(device, completion, readback, default.getTimeout(), default.getTolerance()), parallel )
