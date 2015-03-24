'''
Created on Mar 8,2015
@author: qiuyx
'''
from string import lower
from scan.commands.command import Command
import xml.etree.ElementTree as ET 

class ConfigLog(Command):
    '''
    Config automatic logging.
    '''

    def __init__(self, auto, errhandler=None):
        '''
        @param auto: True to log all write access, False to only log via Log() command.
        Usage::
        >>>cl=ConfigLog(True)
        '''
        self.__auto=auto
        self.__errHandler=errhandler
        
    def genXML(self):
        xml=ET.Element('config_log');
        
        ET.SubElement(xml, 'automatic').text = lower(str(self.__auto))
        #return '<config_log>'+'<automatic>'+lower(str(self.__automatic))+'</automatic>'+'</config_log>'
        
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
             
        return xml
    
    def __repr__(self):
        return self.toCmdString()
        
    def toCmdString(self):
        return 'ConfigLog(%s)' % str(self.__auto)