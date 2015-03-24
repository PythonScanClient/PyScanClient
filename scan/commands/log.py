'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Log(Command):
    '''
    classdocs
    '''


    def __init__(self,errHandler=None,*devices):
        '''
        Constructor
        '''
        self.__devices=[]
        for device in devices:
            self.__devices.append(device)
        self.__errHandler=errHandler
        
    def genXML(self):
        xml = ET.Element('log')
        devices=ET.SubElement(xml, 'devices')
        
        if len(self.__devices)>0:
            for i in range(0,len(self.__devices)):
                ET.SubElement(devices, 'device').text = self.__devices[i]
                
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
            
        return xml
    
    def __repr__(self):
        result = 'Log( '
        for i in range(0,len(self.__devices)):
            result +='device='+self.__devices[i]
            if i!=len(self.__devices)-1:
                result+=', '
        result += ')'
        return result
    
    def toCmdString(self):
        result = 'Log('
        for i in range(0,len(self.__devices)):
            result +='device='+self.__devices[i]
            if i!=len(self.__devices)-1:
                result+=', '
        result += ')'
        return result