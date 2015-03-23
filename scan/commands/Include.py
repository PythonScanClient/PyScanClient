'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET

class Include(Command):
    '''
    classdocs
    '''


    def __init__(self, scanFile=None,macros='macro=value',errHandler=None):
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
        
        ET.SubElement(xml, 'macros').text = self.__macros
        
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
            
        return ET.tostring(xml)
        
    def __repr__(self):
        return 'InclueCommand(scan_file='+self.__scanFile+', macros='+self.__macros+')'
    
    def toCmdString(self):
        return 'InclueCommand(scan_file='+self.__scanFile+', macros='+self.__macros+')'