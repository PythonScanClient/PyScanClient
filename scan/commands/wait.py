'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Wait(Command):
    """Wait until a condition is met, i.e. a device reaches a value.
    
    :param  device:      Name of PV or device.
    :param  value:       Desired value.
    :param  comparison:  How current value is compared to the desired value.
                         Defaults to '='.
                         Other options: '>', '>=', '<' , '<=', 'increase by','decrease by'
    :param  tolerance:  Tolerance used for numeric comparison. Defaults to 0, not used for string values.
    :param  timeout:    Timeout in seconds. Default 0 to wait 'forever'.
    :param  errhandler: Default None.
        
    Example:
        >>> cmd = Wait('shutter', 1)
        >>> cmd = Wait('position', 25.0, timeout=60.0, tolerance=0.5)
        >>> cmd = Wait('counts', 1e12, comparison='>=', timeout=10.0)
        >>> cmd = Wait('counts', 1e12, comparison='increase by',
                       timeout=5.0, errhandler='someHandler')
        
    """
    
    __comparisons= {'=':'EQUALS',
                    '>':'ABOVE',
                    '>=':'AT_LEAST',
                    '<':'BELOW',
                    '<=':'AT_MOST',
                    'increase by':'INCREASE_BY',
                    'decrease by':'DECREASE_BY'}

    def __init__(self, device, value, comparison='=', tolerance=0.0, timeout=0.0, errhandler=None):
        self.__device = device
        self.__desiredValue = value
        if not comparison in Wait.__comparisons:
            raise Exception("Invalid comparison '%s'" % comparison)
        self.__comparison = comparison
        self.__tolerance = tolerance
        self.__timeout = timeout
        self.__errHandler = errhandler
        
    def getDevice(self):
        """:return: Device name"""
        return self.__device

    def setComparison(self, comparison):
        """Change comparison
        
        :param  comparison:  How current value is compared to the desired value.
                             Options: '=', '>', '>=', '<' , '<=', 'increase by','decrease by'
         """
        if not comparison in Wait.__comparisons:
            raise Exception("Invalid comparison '%s'" % comparison)
        self.__comparison = comparison

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
        xml = ET.Element('wait')
        
        ET.SubElement(xml, 'device').text = self.__device
            
        ET.SubElement(xml, 'value').text = str(self.__desiredValue)
        
        ET.SubElement(xml, 'comparison').text = Wait.__comparisons[self.__comparison]
        
        if self.__tolerance > 0.0:
            ET.SubElement(xml,'tolerance').text = str(self.__tolerance)
            
        if self.__timeout > 0.0:
            ET.SubElement(xml,'timeout').text = str(self.__timeout)
            
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = self.__errHandler
            
        return xml
    
    def __repr__(self):
        result = "Wait('%s'" % self.__device
        if isinstance(self.__desiredValue, str):
            result += ", '%s'" % self.__desiredValue
        else:
            result += ", %s" % str(self.__desiredValue)
        if self.__comparison != '=':
            result += ", comparison='%s'" % self.__comparison
        if self.__tolerance > 0:
            result += ', tolerance=%g' % self.__tolerance
        if self.__timeout > 0:
            result += ', timeout=%g' % self.__timeout
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result