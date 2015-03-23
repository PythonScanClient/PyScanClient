"""
Scan settings

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
    def __init__(self, name, completion=False, readback=True, timeout=0.0, tolerance=0.0):
        """name:       Device name
           completion: True to use completion
           readback:   False to not use a readback,
                       True to use the primary name,
                       Actual read back name if different from the promary device name. 
           timeout:    Time out for callback and readback in seconds. 0 to wait forever.
           tolerance:  Tolerance for numeric readback comparison. 
        """
        self.name = name
        self.completion = completion
        self.readback = readback
        self.timeout = timeout
        self.tolerance = tolerance
    
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
    
    def __repr__(self):
        rb = self.getReadback()
        if rb:
            rb = "'" + rb + "'"
        return "DeviceSettings('%s', completion=%s, readback=%s, timeout=%g, tolerance=%g)" % (
                self.name, str(self.completion), rb,  self.timeout, self.tolerance)



class ScanSettings(object):
    """Scan Settings:
       Various lists of devices and how to treat them in a scan
    """

    def __init__(self):
        # List that holds DeviceSettings, but using their 'name' as a regular expression pattern.
        self.device_settings = list()
        
    def defineDeviceClass(self, name_pattern, completion=False, readback=True, timeout=0.0, tolerance=0.0):
        """name_pattern: Device name pattern (regular expression)
           completion:   True to use completion
           readback:     False to not use a readback,
                         True to use the primary name,
                         Actual read back name if different from the promary device name. 
           timeout:      Time out for callback and readback in seconds. 0 to wait forever.
           tolerance:    Tolerance for numeric readback comparison. 
        """
        self.device_settings.append(DeviceSettings(name_pattern, completion, readback, timeout, tolerance))
                        
    def getDeviceSettings(self, name):
        for setting in self.device_settings:
            if re.match(setting.getName(), name):
                return DeviceSettings(name, setting.getCompletion(), setting.getReadback(), setting.getTimeout(), setting.getTolerance())
        return DeviceSettings(name)
    

    def parseDeviceModifiers(self, input):
        """Parse modifiers from device info:
           -r: No readback
           -c: No completion
           +c: Use completion
           +p: parallel
        
           @return: (actual device, completion-or-None, readback-or-None, timeout-or-None,
                     tolerance-or-None, parallel)
        """
        mod_device = input.strip()
        readback = None
        completion = None
        parallel = None
        
        while mod_device.startswith('+') or mod_device.startswith('-'):
            set = mod_device.startswith('+')
            mod_device = mod_device[1:]
            # one or more modifiers may follow the +|-
            while not mod_device[0] in " +-":
                if mod_device[0] == 'r':
                    readback = set
                elif mod_device[0] == 'c':
                    completion = set
                elif mod_device[0] == 'p':
                    parallel = set
                else:
                    raise Exception("Unknown device modifier %s in %s" % (mod_device[0], input))
                mod_device = mod_device[1:]
            mod_device = mod_device.strip()
       
        device = mod_device

        ( def_readback, def_completion, timeout, tolerance ) = self.getDefaults(device)
        # Use defaults unless modifiers were provided
        if def_readback  and readback is None:
            readback = def_readback
        if completion is None:
            completion = def_completion

        # Turn "do use readback" into the device to use,
        # (def_readback would already provide the device)           
        if readback == True:
            readback = device
        
        return (device, completion, readback, timeout, tolerance, parallel)
