'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Comment(Command):
    """Comment
    
    :param text: Comment Text.
        
    Example:
        >>> cmd = Comment("Scan Start.") 
    """
    def __init__(self, text="This is an example comment."):
        self.__text=text
    
    def genXML(self):
        xml=ET.Element('comment');
        ET.SubElement(xml, 'text').text = self.__text
        return xml

    def __repr__(self):
        return "Comment('%s')" % self.__text

    
        