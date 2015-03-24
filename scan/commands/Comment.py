'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET

class Comment(Command):
    '''
    Command to add comment.
    SubClass of Command
    '''
    
    def __init__(self, text="This is an example comment."):
        '''
        @param text: Comment Text.
        
        Usage::
        >>>c=Comment("Scan Start.")
        '''
        self.__text=text
    
    def genXML(self):
        xml=ET.Element('comment');
        ET.SubElement(xml, 'text').text = self.__text
        return xml

    def __repr__(self):
        return self.toCmdString()
    
    def toCmdString(self):
        '''
        Give a printing of this Command. 
        '''
        return "Comment('%s')" % self.__text
    
    
        