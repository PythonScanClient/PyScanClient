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
import sys
import json

from scan.commands.set import Set
from scan.commands.loop import Loop
from scan.commands.wait import Wait

# Dictionary iterator compatible with Python 2 *and* 3
# (See: https://github.com/benjaminp/six/blob/master/six.py#L586)
if sys.version_info[0] == 2:
    def iteritems(d, **kw):
        return d.iteritems(**kw)
else:
    unicode = str
    def iteritems(d, **kw):
        return iter(d.items(**kw))

class DeviceSettings(object):
    """Describes how a device should be accessed in a scan.
    
    :param name:       Device name
    :param completion: True to use completion
    :param readback:   False to not use a readback,
                       True to use the primary name,
                       Actual read back name if different from the promary device name. 
    :param readback_value: None to check against written value, otherwise custom readback number or string value.
    :param timeout:    Time out for callback and readback in seconds. 0 to wait forever.
    :param tolerance:  Tolerance for numeric readback comparison.
    :param comparison: Comparison to use in Wait commands
    :param parallel:   Perform in parallel?
    """
    def __init__(self, name, completion=False, readback=False, readback_value=None, timeout=0.0, tolerance=None, comparison='>=', parallel=False):
        self._name = name
        self._completion = completion
        self._readback = readback
        if isinstance(readback_value, str)  and  len(readback_value) <= 0:
            self._readback_value = None
        else:
            self._readback_value = readback_value
        self._timeout = timeout
        self._tolerance = tolerance
        self._comparison = comparison
        self._parallel = parallel
    
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

    def getReadbackValue(self):
        """:returns: None to check against written value, otherwise custom readback number or string value."""
        return self._readback_value

    def getTimeout(self):
        """:returns: Timeout in seconds for both completion and readback."""
        return self._timeout
    
    def getTolerance(self):
        """:returns: Tolerance for numeric readback check. Does not apply to string values."""
        return self._tolerance

    def getComparison(self):
        """:returns: Comparison for Wait command."""
        return self._comparison

    def getParallel(self):
        """:returns: To be performed in parallel."""
        return self._parallel
    
    def __repr__(self):
        rb = self.getReadback()
        if rb:
            rb = "'" + rb + "'"

        rbv = self._readback_value
        if isinstance(rbv, str):
            rbv = "'" + rbv + "'"

        return "DeviceSettings('%s', completion=%s, readback=%s, readback_value=%s, timeout=%g, tolerance=%s, comparison='%s', parallel=%s)" % (
                self._name, str(self._completion), rb,  rbv, self._timeout, str(self._tolerance), self._comparison, str(self._parallel))



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
        
        # PV that gets updated with the currently executed table scan row
        self.table_scan_row = None
        
    def loadDeviceClasses(self, json_filename):
        """Load device classes from JSON file
        
        :param json_filename: Name of JSON file
        
        Example file content::
            
            {
               ".*daq.*": { "completion": true },
               "pcharge": { comparison": "increase by" },
               "setpoint": { "completion": true, 
                             "tolerance": 0.1, 
                             "readback": "readback"}
            }
        """
        with open(json_filename) as config_file:
            device_config = json.load(config_file)
         
        for dev, attr in iteritems(device_config):
            f = lambda x: x.encode('ascii') if isinstance(x, (unicode, str) ) else x
            self.defineDeviceClass(dev.encode('ascii'), 
                                   completion=attr.get('completion', False),
                                   readback=f(attr.get('readback', False)),
                                   readback_value=f(attr.get('readback_value', "")),
                                   timeout=attr.get('timeout', 0.0),
                                   tolerance=attr.get('tolerance', 0.0),
                                   comparison=attr.get('comparison', ">=")
                                   )

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
        
    def defineDeviceClass(self, name_pattern, completion=False, readback=False, readback_value=None, timeout=0.0, tolerance=None, comparison='>='):
        """Define a class of devices based on name
        
        Call this in the constructor of your derived class.
        
        The order of registration matters.
        First, define generic settings, for example for ".*" to set the general defaults.
        Then register more and more specific patterns,
        until eventually registering specific device names.
        
        :param name_pattern: Device name pattern (regular expression)
        :param completion:   True to use completion
        :param readback:     False to not use a readback,
                             True to use the primary name,
                             Actual read back name if different from the promary device name. 
        :param readback_value: None to check against written value, otherwise custom readback number or string value.
        :param timeout:      Time out for callback and readback in seconds. 0 to wait forever.
        :param tolerance:    Tolerance for numeric readback comparison.
        :param comparison:   Comparison to use in Wait commands.
        """
        self.device_settings.insert(0, DeviceSettings(name_pattern, completion=completion, readback=readback, readback_value=readback_value, timeout=timeout, tolerance=tolerance, comparison=comparison))                
                        
    def getDefaultSettings(self, name):
        """Get the default settings for a device
        
        :param name: Name of device
        :return: DeviceSettings for that device.
        """
        for setting in self.device_settings:
            # Look for full match, as if pattern used "^whatever$".
            # re.match() implies the "^..", we assert the " ..$"
            m = re.match(setting.getName(), name)
            if (m is not None) and (m.group(0) == name):
                # rb = False (no readback), True (use device name), or "SomeExactName" 
                rb = setting._readback
                if rb == True:
                    rb = self.getReadbackName(name)
                return DeviceSettings(name, completion=setting.getCompletion(), readback=rb, readback_value=setting.getReadbackValue(), timeout=setting.getTimeout(), tolerance=setting.getTolerance(), comparison=setting.getComparison())
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
        :return: DeviceSettings
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
        
        return DeviceSettings(default.getName(), completion=completion, readback=readback, readback_value=default.getReadbackValue(),
                              timeout=default.getTimeout(), tolerance=default.getTolerance(),
                              comparison=default.getComparison(), parallel=parallel)

    def __str__(self):
        return str(self.device_settings)

__scan_settings = ScanSettings()

def getScanSettings():
    """:return: Global scan settings"""
    return __scan_settings

def setScanSettings(settings):
    """Set global scan settings
    :param settings: Desired global scan settings
    """
    global __scan_settings
    __scan_settings = settings


def SettingsBasedSet(prefixed_device, value, **kwargs):
    """Set a device to a value.
    
    :param device:     Device name
    :param value:      Value

    Defaults to :class:`~scan.util.scan_settings.ScanSettings`,
    but allows overrides for the following parameters:
    
    :param completion: Await callback completion?
    :param readback:   `False` to not check any readback,
                       `True` to wait for readback from the `device`,
                       or name of specific device to check for readback.
    :param readback_value: None to check against written value, otherwise custom readback number or string value.
    :param tolerance:  Tolerance when checking numeric `readback`.
    :param timeout:    Timeout in seconds, used for `completion` and `readback`.
    :param errhandler: Error handler
    """
    settings = __scan_settings.parseDeviceSettings(prefixed_device)
    completion = kwargs['completion'] if 'completion' in kwargs else settings.getCompletion()
    readback   = kwargs['readback'] if 'readback' in kwargs else settings.getReadback()
    readback_value = kwargs['readback_value'] if 'readback_value' in kwargs else settings.getReadbackValue()
    tolerance  = kwargs['tolerance'] if 'tolerance' in kwargs else settings.getTolerance()
    timeout    = kwargs['timeout'] if 'timeout' in kwargs else settings.getTimeout()
    errhandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
    
    if tolerance is None:
        tolerance = 0.1

    return Set(settings.getName(), value,
               completion=completion, readback=readback, readback_value=readback_value, tolerance=tolerance, timeout=timeout, errhandler=errhandler)

def SettingsBasedLoop(prefixed_device, start, end, step, body=None, *args, **kwargs):
    """Set a device to various values in a loop.
    
    Optional check of completion and readback verification.
    
    :param device:     Device name
    :param start:      Initial value
    :param end:        Final value
    :param step:       Step size
    :param body:       One or more commands

    Defaults to :class:`~scan.util.scan_settings.ScanSettings`,
    but allows overrides for the following parameters:

    :param completion: Await callback completion?
    :param readback:   `False` to not check any readback,
                       `True` to wait for readback from the 'device',
                       or name of specific device to check for readback.
    :param tolerance:  Tolerance when checking numeric `readback`.
                       Defaults to 0.
    :param timeout:    Timeout in seconds, used for `completion` and `readback` check.
    :param errhandler: Error handler
    """
    settings = __scan_settings.parseDeviceSettings(prefixed_device)
    completion = kwargs['completion'] if 'completion' in kwargs else settings.getCompletion()
    readback   = kwargs['readback'] if 'readback' in kwargs else settings.getReadback()
    tolerance  = kwargs['tolerance'] if 'tolerance' in kwargs else settings.getTolerance()
    timeout    = kwargs['timeout'] if 'timeout' in kwargs else settings.getTimeout()
    errhandler = kwargs['errhandler'] if 'errhandler' in kwargs else None

    if tolerance is None:
        tolerance = abs(step)/10.0
    
    return Loop(settings.getName(), start, end, step, body, *args,
                completion=completion, readback=readback, tolerance=tolerance, timeout=timeout, errhandler=errhandler)
                

def SettingsBasedWait(prefixed_device, value, **kwargs):
    """Wait until a condition is met, i.e. a device reaches a value.
    
    :param  device:      Name of PV or device.
    :param  value:       Desired value.

    Defaults to :class:`~scan.util.scan_settings.ScanSettings`,
    but allows overrides for the following parameters:

    :param  comparison:  How current value is compared to the desired value.
                         Options: '=', '>', '>=', '<' , '<=', 'increase by','decrease by'
    :param  tolerance:  Tolerance used for numeric comparison. Defaults to 0, not used for string values.
    :param  timeout:    Timeout in seconds. Default 0 to wait 'forever'.
    :param  errhandler: Default None.
    """
    settings = __scan_settings.parseDeviceSettings(prefixed_device)
    comparison = kwargs['comparison'] if 'comparison' in kwargs else settings.getComparison()
    tolerance  = kwargs['tolerance'] if 'tolerance' in kwargs else settings.getTolerance()
    timeout    = kwargs['timeout'] if 'timeout' in kwargs else settings.getTimeout()
    errhandler = kwargs['errhandler'] if 'errhandler' in kwargs else None

    if tolerance is None:
        tolerance = 0.1

    return Wait(settings.getName(), value,
                comparison=comparison, tolerance=tolerance, timeout=timeout, errhandler=errhandler)
