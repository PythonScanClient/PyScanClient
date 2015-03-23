'''
Created on Mar 8,2015
@author: qiuyx
'''
from string import lower
from scan.commands.Command import Command
import xml.etree.ElementTree as ET 

class ConfigLog(Command):
    '''
    Config atuomatic logging.
    '''


    def __init__(self, auto=False,errHandler=None):
        '''
        @param auto: True or False for whether logging is automatic.
                     Defaults as False.
        
        Usage::
        >>>cl=ConfigLog(True)
        '''
        self.__auto=auto
        self.__errHandler=errHandler
        
    def genXML(self):
        xml=ET.Element('config_log');
        
        ET.SubElement(xml, 'automatic').text = lower(str(self.__auto))
        #return '<config_log>'+'<automatic>'+lower(str(self.__automatic))+'</automatic>'+'</config_log>'
        
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
        
        r=ET.tostring(xml)
        
        return r
    
    def __repr__(self):
        return 'ConfigLogCommand(Automatic='+lower(str(self.__auto))+')'
        
    def toCmdString(self):
        return 'ConfigLogCommand(Automatic='+lower(str(self.__auto))+')'