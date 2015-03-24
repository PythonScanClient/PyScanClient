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

    def __init__(self, devices=None, *args, **kwargs):
        """Examples:
         
           Log()
           Log("pv1")
           Log("pv1", "pv2")
           Log(devices=["pv1", "pv2"])
           Log(devices=["pv1", "pv2"], errHandler="OnErrorContinue")
        """
        if isinstance(devices, str):
            self.__devices = [ devices ]
        elif devices:
            self.__devices = list(devices)
        else:
            self.__devices = list()
        if args:
            self.__devices += args
        self.__errHandler = kwargs['errHandler'] if 'errHandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('log')
        
        if len(self.__devices)>0:
            devices=ET.SubElement(xml, 'devices')
            for dev in self.__devices:
                ET.SubElement(devices, 'device').text = dev
                
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
            
        return xml
    
    def __repr__(self):
        result = 'Log('
        if len(self.__devices):
            result += "'"
            result += "', '".join(self.__devices)
            result += "'"
        if self.__errHandler:
            result += ", errHandler='%s'" % self.__errHandler
        result += ')'
        return result
    
    def toCmdString(self):
        return self.__repr__()
    