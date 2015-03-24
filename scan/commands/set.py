'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Set(Command):
    '''
    classdocs
    '''

    def __init__(self, device, value, completion=False, readback=False, tolerance=0.0, timeout=0.0, errhandler=None):
        '''
        Command to set a device to a value, with optional check of completion and readback verification.
        @param device:     Device name
        @param value:      Value
        @param completion: Await __completion?
        @param readback:   False to not check any readback,
                           True to wait for readback from the 'device',
                           or name of specific device to check for readback.
        @param tolerance:  Tolerance when checking numeric readback.
        @param timeout:    Timeout in seconds, used for 'completion' and 'readback' check
        @param errhandler: Error handler
        '''
        self.__device=device
        self.__value=value
        self.__completion=completion
        self.__readback=readback
        self.__tolerance=tolerance
        self.__timeout=timeout
        self.__errHandler=errhandler
        
    def genXML(self):
        xml = ET.Element('set')

        dev=ET.SubElement(xml, 'device')
        if self.__device:
            dev.text = self.__device
            
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
        if need_timeout  and  self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)
        
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = self.__errHandler
 
        return xml
    
    def __repr__(self):
        return self.toCmdString()
    
    def toCmdString(self):
        result = "Set('%s'" % self.__device
        if isinstance(self.__value, str):
            result += ", value='%s'" % self.__value
        else:
            result += ", value=%s" % str(self.__value)
        if self.__completion:
            result += ', completion=true'
        if isinstance(self.__readback, str):
            result += ", readback='%s'" % self.__readback
        elif self.__readback:
            result += ", readback=%s" % str(self.__readback)
        if self.__timeout!=0.0:
            result += ', timeOut='+str(self.__timeout)
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result+=')'
        return result
    
        