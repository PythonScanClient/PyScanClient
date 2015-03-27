"""
Scan settings
=============

Provides information on how to access a device.

* Wait for callback completion?
* Check a readback?

  * Which one? The original device, or a different one?
  * Look for exact match, or use a tolrance of +- 0.5?
  
* With what timeout?

When installing the scan client library,
derive your site-specific implementation
from the ScanSettings class
and make it available to all users of this library.


Example
-------

.. literalinclude:: ../example/scan_settings1.py

API
---
"""
#@author: Kay Kasemir
import re

from scan.commands.set import Set
from scan.commands.wait import Wait

class DeviceSettings(object):
    """Describes how a device should be accessed in a scan.
    
    :param name:       Device name
    :param completion: True to use completion
    :param readback:   False to not use a readback,
                       True to use the primary name,
                       Actual read back name if different from the promary device name. 
    :param timeout:    Time out for callback and readback in seconds. 0 to wait forever.
    :param tolerance:  Tolerance for numeric readback comparison.
    :param comparison: Comparison to use in Wait commands
    """
    def __init__(self, name, completion=False, readback=False, timeout=0.0, tolerance=0.0, comparison='>='):
        self._name = name
        self._completion = completion
        self._readback = readback
        self._timeout = timeout
        self._tolerance = tolerance
        self._comparison = comparison
    
    def getName(self):
        """:returns: Device name."""
        return self._name

    def getCompletion(self):
        """:returns: True when device should be accessed with completion."""
        return self._completion

    def getReadback(self):
        """:returns: Device name to use for readback, or None."""
        if not self._readback:
            return None
        return self._name if self._readback == True else self._readback

    def getTimeout(self):
        """:returns: Timeout in seconds for both completion and readback."""
        return self._timeout
    
    def getTolerance(self):
        """:returns: Tolerance for numeric readback check. Does not apply to string values."""
        return self._tolerance

    def getComparison(self):
        """:returns: Comparison for Wait command."""
        return self._comparison
    
    def Set(self, value):
        """Create `Set` command.
        
        Creates a `Set` command that sets a device to
        the desired value, using completion, readback etc.
        as per these device settings.
        
        :param value: Desired value
        :return: :class:`scan.commands.set.Set` command.
        """
        return Set(self.getName(), value,
                   completion=self.getCompletion(),
                   readback=self.getReadback(),
                   timeout=self.getTimeout(),
                   tolerance=self.getTolerance())

    def Wait(self, value, timeout=None, errhandler=None):
        """Create `Wait` command.
        
        Creates a `Wait` command for this device,
        using comparison and timeout
        as per these device settings.
        
        :param value: Desired value
        :param timeout: Optional timeout in seconds to override `DeviceSettings`.
        :param errhandler: Optional error handler
          
        :return: :class:`scan.commands.wait.Wait` command.
        """
        if timeout is None:
            timeout = self._timeout
        return Wait(self.getName(), value,
                    comparison=self.getComparison(),
                    tolerance=self.getTolerance(),
                    timeout=timeout,
                    errhandler=errhandler)

    
    def __repr__(self):
        rb = self.getReadback()
        if rb:
            rb = "'" + rb + "'"
        return "DeviceSettings('%s', completion=%s, readback=%s, timeout=%g, tolerance=%g, comparison='%s')" % (
                self._name, str(self._completion), rb,  self._timeout, self._tolerance, self._comparison)



class ScanSettings(object):
    """Base class for site-specific scan settings
    """

    def __init__(self):
        # List that holds DeviceSettings, but NOT exactly as it's passed out to
        # uses of this class:
        # The device_settings[].name is a regular expression pattern for device names.
        self.device_settings = list()
        
        # In derived class, may register special behavior for certain devices
        # self.defineDeviceClass("My:Motor.*", completion=True, readback=True, timeout=100)

    def getReadbackName(self, device_name):
        """Override this method to provide custom readback names.
        
        For example, map from device names that match the naming
        convention for motors at your site and return the associated
        `*.RBV` name.
           
        :param device_name: Primary device name
        :return: Corresponding device name for readback check
        """
        
        # Example for derived class:
        #if "Motor" in device_name:
        #    return device_name + ".RBV"
        
        return device_name
        
    def defineDeviceClass(self, name_pattern, completion=False, readback=False, timeout=0.0, tolerance=0.0, comparison='>='):
        """Define a class of devices based on name
        
        Call this in the constructor of your derived class.
        
        :param name_pattern: Device name pattern (regular expression)
        :param completion:   True to use completion
        :param readback:     False to not use a readback,
                             True to use the primary name,
                             Actual read back name if different from the promary device name. 
        :param timeout:      Time out for callback and readback in seconds. 0 to wait forever.
        :param tolerance:    Tolerance for numeric readback comparison.
        :param comparison:   Comparison to use in Wait commands.
        """
        self.device_settings.append(DeviceSettings(name_pattern, completion, readback, timeout, tolerance, comparison))                
                        
    def getDefaultSettings(self, name):
        """Get the default settings for a device
        
        :param name: Name of device
        :return: DeviceSettings for that device.
        """
        for setting in self.device_settings:
            if re.match(setting.getName(), name):
                # rb = False (no readback), True (use device name), or "SomeExactName" 
                rb = setting._readback
                if rb == True:
                    rb = self.getReadbackName(name)
                return DeviceSettings(name, setting.getCompletion(), rb, setting.getTimeout(), setting.getTolerance(), setting.getComparison())
        return DeviceSettings(name)
    
    def parseDeviceSettings(self, prefixed_device):
        """Parse a device name that may be prefixed with modifiers.
        
        For example, the name 'SomeMotor' may ordinarily indicate a
        motor and by default be accessed with callback completion
        and readback if you called `parseDeviceSettings('SomeMotor')`.
        
        By adding the prefix '-c-r' or '-cr', the DeviceSettings will
        exclude the completion and readback:
        `parseDeviceSettings('-cr SomeMotor')`.
        
           
        Supported modifiers:
        
        * -c: Do not await completion
        * +c: Do await completion
        * -r: Do not check readback
        * +r: Do check readback
        * +p: Access in parallel

        :param prefixed_device: Name of device with optional prefixes
        :return: ( DeviceSettings, parallel )
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

    def Set(self, prefixed_device, value):
        """Create `Set` command.
        
        Creates a `Set` command that sets a device to
        the desired value, using completion, readback etc.
        as per these settings.
        
        :param prefixed_device: Device name with optional prefixes
        :param value: Desired value
        :return: :class:`scan.commands.set.Set` command.
        """
        (device, ignored) = self.parseDeviceSettings(prefixed_device)
        return device.Set(value)

    def Wait(self, device, value, timeout=None, errhandler=None):
        """Create `Wait` command.
        
        Creates a `Wait` command for this device,
        using comparison and timeout
        as per these settings.
        
        :param device: Device name
        :param value: Desired value
        :param timeout: Optional timeout in seconds to override `ScanSettings`.
        :param errhandler: Optional error handler
          
        :return: :class:`scan.commands.wait.Wait` command.
        """
        settings = self.getDefaultSettings(device)
        return settings.Wait(value, timeout, errhandler)

