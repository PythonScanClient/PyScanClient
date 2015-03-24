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

    def __init__(self, device=None,value=0.0,completion=False,readback=False,tolerance=0.1,timeout=0.0,errhandler=None):
        '''
        command to set a __device to a __value
        @param __device: Device name
        @param __value: Value
        @param __completion: Await __completion?
        @param __readback: False to not check any __readback.
                         True to __wait for __readback from the '__device',
                         or name of specific __readback different from '__device'.
        @param __tolerance: Readback __tolerance
        @param timeout: Timeout in seconds, used for __completion and __readback check
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
        if self.__device!=None:
            dev.text = self.__device
            
        ET.SubElement(xml, 'value').text = str(self.__value)
        
        need_timeout = False
        if self.__completion==True:
            ET.SubElement(xml, 'completion').text = 'true'
            need_timeout = True
            
        if self.__readback:
            ET.SubElement(xml, "wait").text = "true"
            ET.SubElement(xml, "readback").text = self.__device if self.__readback == True else self.__readback
            ET.SubElement(xml, "tolerance").text = str(self.__tolerance)
            need_timeout = True
        if need_timeout  and  self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)
        
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
 
        return xml
    
    def __repr__(self):
        return self.toCmdString()
    
    def toCmdString(self):
        result = "Set('%s'" % self.__device
        if isinstance(self.__value, str):
            result += ",value='%s'" % self.__value
        else:
            result += ",value=%s" % str(self.__value)
        if self.__completion:
            result += ',completion=true'
        if isinstance(self.__readback, str):
            result += ", readback='%s'" % self.__readback
        elif self.__readback:
            result += ", readback=%s" % str(self.__readback)
        if self.__timeout!=0.0:
            result += ',timeOut='+str(self.__timeout)
        result+=')'
        return result
    
        