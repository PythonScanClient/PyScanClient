'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class Set(Command):
    """Set a device to a value.
    
    With optional check of completion and readback verification.
    
    :param device:     Device name
    :param value:      Value
    :param completion: Await callback completion?
    :param readback:   `False` to not check any readback,
                       `True` to wait for readback from the `device`,
                       or name of specific device to check for readback.
    :param tolerance:  Tolerance when checking numeric `readback`.
    :param timeout:    Timeout in seconds, used for `completion` and `readback`.
    :param errhandler: Error handler
    
    Example:
        >>> cmd = Set('position', 10.5)

    *Note usage of timeout:*
    When the command awaits completion, the timeout is applied to the completion check,
    i.e. we await the completion callback for `timeout` seconds.
    If another readback check is performed after the completion,
    this check is immediate, comparing the readback right now,
    and not waiting for the readback to match within another `timeout` seconds.

    On the other hand, if completion is not used,
    the timeout is applied to the readback check.
    So in case a readback comparison is requested,
    we wait for up to `timeout` seconds for the readback to be within tolerance.    

    *Note use of completion:*
    EPICS Channel Access does not communicate if completion ('put-callback') is actually
    supported. When writing to a PV that does not support completion, the call is returned
    right away, just as it would for a PV that supports completion and happens to complete
    quickly.
    Similarly, a PV that supports completion will only tell us when it's 'done',
    no matter if it completed successfully, or if it eventually gave up and completed
    without actually reaching the desired setpoint.

    **Use case 1: Neither completion nor readback**

    The `Set` command simply writes to the device.

    This would be suitable for a write-and-forget PV.
    For example, a PV that turns a power supply on or off, and
    the device reacts quasi immediately.

    **Use case 2: No completion, but readback**

    The `Set` command writes to the device, and uses the `timeout`
    to wait for the readback to match the written value.

    This can be sufficient for simple, well behaved devices,
    but can be problematic for a device where the readback will
    take time to settle. Examples include PID-controlled devices
    with overshoot and settling time, or motors with backlash compensation
    and retries where the readback might early on be close to the setpoint,
    but it has not settled, so we consider it 'done' when in fact the
    device is actively changing its value.

    **Use case 3: Enable completion but no readback**

    The `Set` command writes to the device, then uses the `timeout`
    to wait for the completion confirmation.

    This can be used with PVs that support completion and are dependable.
    We cannot distinguish between a completion that is successful,
    versus completion as a result of the device giving up.

    If this mode is by accident used with a PV that doesn't actually
    support completion, the IOC will immediately confirm the completion,
    behaving just like case 1.

    **Use case 4: Enable completion and readback**
    
    This is the ideal case, which is for example supported by the 'motor' record
    or EPICS databases for Lakeshore controllers.
    The `Set` command writes to the device, waits for the completion (based on timeout),
    and then compares the written value against the `readback` PV to check
    if we completed successfully, or if the device completed without being able to
    actually reach the setpoint.

    Note that this must *only be used with devices that actually support completion*.
    When applied to a plain PV that does not support completion,
    we will immediately receive the completion confirmation,
    then check the readback, which is very likely not matching the setpoint, yet,
    and fail.
    So while this is best for PVs that support completion, it is worst for PVs
    that don't.

    Unfortunately there is no way in EPICS to determine the 'correct' settings
    for a PV without knowing how it is implemented on the IOC, so the
    choice of completion, readback and timeout needs to be configured by somebody
    who knows the PV's behavior.
    """

    def __init__(self, device, value, completion=False, readback=False, tolerance=0.0, timeout=0.0, errhandler=None):
        self.__device = device
        self.__value = value
        self.__completion = completion
        self.__readback = readback
        self.__tolerance = tolerance
        self.__timeout = timeout
        self.__errHandler = errhandler
        
    def getDevice(self):
        """:return: Device name"""
        return self.__device
    
    def setCompletion(self, completion):
        """Change completion
        
        :param completion: Await callback completion?
        """
        self.__completion = completion

    def setReadback(self, readback):
        """Change readback
        
        :param readback: `False` to not check any readback,
               `True` to wait for readback from the `device`,
               or name of specific device to check for readback.
        """
        self.__readback = readback

    def setTolerance(self, tolerance):
        """Change tolerance
        
        :param tolerance:  Tolerance when checking numeric `readback`.
        """
        self.__tolerance = tolerance

    def setTimeout(self, timeout):
        """Change timeout
        
        :param timeout:    Timeout in seconds, used for `completion` and `readback`.
        """
        self.__timeout = timeout
        
    def genXML(self):
        xml = ET.Element('set')

        dev = ET.SubElement(xml, 'device')
        if self.__device:
            dev.text = self.__device
        
        if isinstance(self.__value, str):
            ET.SubElement(xml, 'value').text = '"%s"' % self.__value
        else:
            ET.SubElement(xml, 'value').text = str(self.__value)
        
        need_timeout = False
        if self.__completion:
            ET.SubElement(xml, 'completion').text = 'true'
            need_timeout = True
            
        if self.__readback:
            ET.SubElement(xml, "wait").text = "true"
            ET.SubElement(xml, "readback").text = self.__device if self.__readback == True else self.__readback
            ET.SubElement(xml, "tolerance").text = str(self.__tolerance)
            need_timeout = True
        else:
            ET.SubElement(xml, "wait").text = "false"            
        if need_timeout  and  self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)
        
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = self.__errHandler
 
        return xml
    
    def __repr__(self):
        result = "Set('%s'" % self.__device
        if isinstance(self.__value, str):
            result += ", '%s'" % self.__value
        elif isinstance(self.__value, float):
            # Reproduce the default floating point number format provided by Python 2 (and 3.1)
            # (See: https://stackoverflow.com/questions/25898733/why-does-strfloat-return-more-digits-in-python-3-than-python-2/25899600#25899600)
            if self.__value.is_integer():
                result += ", %.12g.0" % self.__value
            else:
                result += ", %.12g" % self.__value
        else:
            result += ", %s" % str(self.__value)
        if self.__completion:
            result += ', completion=True'
            if self.__timeout!=0.0:
                result += ', timeout='+str(self.__timeout)
        if isinstance(self.__readback, str):
            result += ", readback='%s'" % self.__readback
            result += ", tolerance=%f" % self.__tolerance
            if not self.__completion and  self.__timeout!=0.0:
                result += ', timeout='+str(self.__timeout)
        elif self.__readback:
            result += ", readback=%s" % str(self.__readback)
            result += ", tolerance='%f'" % self.__tolerance
            if not self.__completion and  self.__timeout!=0.0:
                result += ', timeout='+str(self.__timeout)
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result+=')'
        return result
    
        
