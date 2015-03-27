'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET 

class Delay(Command):
    """Delay for a fixed amount of time
    
    :param seconds: Time to delay in seconds. 
        
    Example:
        >>> cmd = Delay(2.5)
    """
    def __init__(self, seconds, errhandler=None):
        self.__seconds = seconds
        self.__errHandler = errhandler
    
    def genXML(self):
        xml = ET.Element('delay')
        ET.SubElement(xml, 'seconds').text = str(self.__seconds)
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
        return xml
    
    def __repr__(self):
        result = "Delay(%g" % self.__seconds
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result+=')'
        return result

