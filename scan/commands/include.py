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


    def __init__(self, scan, macros=None, errhandler=None):
        '''
        @param scan:   Name of included scan file, must be on the server's list of script_paths
        @param macros: "name=value, other=42"
        
        Usage::
        >>>icl=Include(scanFile='PrepMotor.scn', macros='macro=value')
        '''
        self.__scanFile = scan
        self.__macros = macros
        self.__errHandler = errhandler
    
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
            result += ", errhandler='%s'" % self.__errHandler
        result += ")"
        return result
            