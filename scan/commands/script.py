'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Script(Command):
    '''
    classdocs
    '''

    def __init__(self, path='the_script.py', *args, **kwargs):
        '''
        Example:
        Script("MyCustomCommand")
        Script("MyCustomCommand", "arg1", 42.3)
        '''
        self.__path = path
        self.__args = args
        self.__errHandler = kwargs['errHandler'] if 'errHandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('script')
        ET.SubElement(xml, 'path').text = self.__path

        if len(self.__args)!=0:
            argLst = ET.SubElement(xml, 'arguments')
            for arg in self.__args:
                ET.SubElement(argLst,'argument').text = str(arg)
        
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                
        return xml
    
    def __repr__(self):
        return self.toCmdString()
        
    def toCmdString(self):
        result= "Script('%s'" % self.__path
        for arg in self.__args:
            if isinstance(arg, str):
                result += ", '%s'" % arg
            else:
                result += ", " + str(arg)
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result+=')'
        return result