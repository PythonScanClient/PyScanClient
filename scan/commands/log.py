'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class Log(Command):
    """Log current value of one or more devices.
    
    :param devices: One or more devices to log
    
    The current value of listed devices is logged with the scan
    and can later be retrieved.
    
    The logged data is meant to allow tracking the progress
    of the scan or to debug details of a scan.
    It does not provide data acquisition.
    
    Examples:
        >>> cmd = Log()
        >>> cmd = Log("pv1")
        >>> cmd = Log("pv1", "pv2")
        >>> cmd = Log(devices=["pv1", "pv2"])
        >>> cmd = Log(devices=["pv1", "pv2"], errhandler="OnErrorContinue")
    """
    def __init__(self, devices=None, *args, **kwargs):
        if isinstance(devices, str):
            self.__devices = [ devices ]
        elif devices:
            self.__devices = list(devices)
        else:
            self.__devices = list()
        if args:
            self.__devices += args
        self.__errHandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('log')
        
        if len(self.__devices)>0:
            devices=ET.SubElement(xml, 'devices')
            for dev in self.__devices:
                ET.SubElement(devices, 'device').text = dev
                
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
            
        return xml
    
    def __repr__(self):
        result = 'Log('
        if len(self.__devices):
            result += "'"
            result += "', '".join(self.__devices)
            result += "'"
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result
    
