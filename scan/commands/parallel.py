'''
Parallel Command

@author: Kay Kasemir
'''
from scan.commands import Command
import xml.etree.ElementTree as ET 

class Parallel(Command):
    def __init__(self, body=None, *args, **kwargs):
        """Examples:
        
           Parallel()
           Parallel(command1)
           Parallel(command1, command2)
           Parallel(body=[command1, command2])
           Parallel(body=[command1, command2], timeout=10, errHandler="MyErrorHandler")
        """
        if isinstance(body, Command):
            self.__body = [ body ]
        elif body:
            self.__body = list(body)
        else:
            self.__body = list()
        if args:
            self.__body += args
        self.__timeout = kwargs['timeout'] if 'timeout' in kwargs else 0
        self.__errHandler = kwargs['errHandler'] if 'errHandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('parallel')
        
        if self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)

        if len(self.__body)!=0:
            body = ET.SubElement(xml,'body')
            for Command in self.__body:
                body.append(Command.genXML())
                
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                          
        return xml
    
    def __repr__(self):
        return self.toCmdString()
        
    def toCmdString(self):
        result = 'Parallel('
        result += ", ".join([ cmd.toCmdString() for cmd in self.__body ])
        if self.__timeout > 0:
            result += ', timeout=%g' % self.__timeout
        if self.__errHandler:
            result += ", errHandler='%s'" % self.__errHandler
        result += ')'
        return result
