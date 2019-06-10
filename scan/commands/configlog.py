'''
Created on Mar 8,2015
@author: qiuyx
'''
from string import lower
from scan.commands.command import Command
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class ConfigLog(Command):
    """Config automatic logging.
    
    :param auto: `True` to log all write access, `False` to only log via `Log()` command.
    
    Example:
        >>> cmd = ConfigLog(True)
    """
    def __init__(self, auto, errhandler=None):
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
        return 'ConfigLog(%s)' % str(self.__auto)
