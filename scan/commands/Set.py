'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET

class Set(Command):
    '''
    classdocs
    '''


    def __init__(self, device=None,value=0.0,completion=False,readback=False,tolerance=0.1,timeout=0.0,errhandler=None):
        '''
        Command to set a __device to a __value
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
        self.__timeOut=timeout
        self.__errHandler=errhandler
        
    def genXML(self):
        xml = ET.Element('set')

        dev=ET.SubElement(xml, 'device')
        if self.__device!=None:
            dev.text = self.__device
            
        ET.SubElement(xml, 'value').text = str(self.__value)
        
        if self.__completion==True:
            ET.SubElement(xml, 'completion').text = 'true'
            need_timeout = True
            
        if self.readback:
            ET.SubElement(xml, "wait").text = "true"
            ET.SubElement(xml, "readback").text = self.__device if self.__readback == True else self.__readback
            ET.SubElement(xml, "tolerance").text = str(self.__tolerance)
            need_timeout = True
        if need_timeout  and  self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)
        
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
 
        return ET.tostring(xml)
    
    def __repr__(self):
        result= 'Set( device='+self.__device
        result+= ', value='+str(self.__value)
        if self.__completion==True:
            result+=', completion=true'
        if self.__wait==False:
            result+=', wait=false'
        if self.__timeOut!=0.0:
            result+=', timeOut='+str(self.__timeOut)
        result+=')'
        return result
    
    def toCmdString(self):
        result= 'Set(device='+self.__device
        result+= ',value='+str(self.__value)
        if self.__completion==True:
            result+=',completion=true'
        if self.__wait==False:
            result+=',wait=false'
        if self.__timeOut!=0.0:
            result+=',timeOut='+str(self.__timeOut)
        result+=')'
        return result
    
        