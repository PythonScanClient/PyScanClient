'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Include(Command):
    """Include another scan.
    
    Allows re-use of existing scans within a larger scan.
    The included scan can use "$(macro)" for device names.
    
    :param scan:   Name of scan file.
                   Must contain valid scan in XML format
                   and be on the server's list of script_paths.
    :param macros: "name=value, other=42"
        
    Example::
        >>> cmd = Include('PrepMotor.scn', macros='motor=MyMotor1')
    """
    def __init__(self, scan, macros=None, errhandler=None):
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
        result = "Include('%s'" % self.__scanFile
        if self.__macros:
            result += ", macros='%s'" % self.__macros
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result += ")"
        return result
            