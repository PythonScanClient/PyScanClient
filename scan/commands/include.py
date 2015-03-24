'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Include(Command):
    '''
    classdocs
    '''


    def __init__(self, scanFile=None, macros=None,errHandler=None):
        '''
        @param scanFile: The included scan file path located at /scan/example
                         Defaults as None.
        @param macros:   
        
        Usage::
        >>>icl=Include(scanFile='PrepMotor.scn',macros='macro=value')
        '''
        self.__scanFile=scanFile
        self.__macros=macros
        self.__errHandler=errHandler
    
    def genXML(self):
        xml = ET.Element('include')
        
        ET.SubElement(xml, 'scan_file').text = self.__scanFile
        if self.__macros:
            ET.SubElement(xml, 'macros').text = self.__macros
        
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = self.__errHandler
            
        return xml
        
    def __repr__(self):
        return self.toCmdString()
    
    def toCmdString(self):
        result = "Include('%s'" % self.__scanFile
        if self.__macros:
            result += ", macros='%s'" % self.__macros
        if self.__errHandler:
            result += ", errHandler='%s'" % self.__errHandler
        result += ")"
        return result
            