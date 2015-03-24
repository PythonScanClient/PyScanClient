'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET 

class Delay(Command):
    '''
    classdocs
    '''

    def __init__(self, seconds, errhandler=None):
        '''
        @param seconds: Time to delay in seconds. 
        
        Usage::
        >>>dl=Delay(2.5)
        '''
        self.__seconds = seconds
        self.__errHandler = errhandler
    
    def genXML(self):
        xml = ET.Element('delay')
        ET.SubElement(xml, 'seconds').text = str(self.__seconds)
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
        return xml
    
    def __repr__(self):
        return self.toCmdString()
    
    def toCmdString(self):
        result = "Delay(%g" % self.__seconds
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result+=')'
        return result

