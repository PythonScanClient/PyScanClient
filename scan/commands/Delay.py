'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET 

class Delay(Command):
    '''
    classdocs
    '''

    def __init__(self, seconds=1.0,errHandler=None):
        '''
        @param seconds: Time to delay. 
                        Defaults as 1.0
        
        Usage::
        >>>dl=Delay(2.5)
        '''
        self.__seconds=seconds
        self.__errHandler=errHandler
    
    def genXML(self):
        xml = ET.Element('delay')
        
        ET.SubElement(xml, 'seconds').text = str(self.__seconds)
        #return '<delay>'+'<seconds>'+str(self.__seconds)+'</seconds>'+'</delay>'
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
            
        return xml
    
    def __repr__(self):
        return 'DelayCommand(seconds='+str(self.__seconds)+')'
    
    def toCmdString(self):
        return 'DelayCommand(seconds='+str(self.__seconds)+')'
