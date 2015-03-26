'''
Parallel Command

@author: Kay Kasemir
'''
from scan.commands import Command
import xml.etree.ElementTree as ET 

class Parallel(Command):
    """Perform multiple commands in parallel.
    
    Each of the commands performed in parallel may await
    callback completion and/or check readbacks.
    
    The `Parallel` command completes when all of the commands
    in its `body` have finished executing,
    or an optional timeout expires.
    
    :param body:       Commands or list of commands
    :param timeout:    Optional timeout in seconds.
                       By default, wait forever.
    :param errhandler: Optional error handler.
    
    Examples:
    
    Do nothing:
        >>> cmd = Parallel()
        
    Perform one command, same as directly using `Set('x', 1)`:
        >>> cmd = Parallel(Set('x', 1))
    
    Set two PVs to a value, each awaiting callback completion:
        >>> cmd = Parallel(Set('x', 1, completion=True),
        ...                Set('y', 2, completion=True))
    
    Given a list of commands, perform them all in parallel:
        >>> cmd = Parallel(body=[command1, command2, command3])
        
    .. with timeout:
        >>> cmd = Parallel(body=[command1, command2], timeout=10)
    """
    def __init__(self, body=None, *args, **kwargs):
        if isinstance(body, Command):
            self.__body = [ body ]
        elif body:
            self.__body = list(body)
        else:
            self.__body = list()
        if args:
            self.__body += args
        self.__timeout = kwargs['timeout'] if 'timeout' in kwargs else 0
        self.__errHandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('parallel')
        
        if self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)

        if len(self.__body)!=0:
            body = ET.SubElement(xml,'body')
            for cmd in self.__body:
                body.append(cmd.genXML())
                
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
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result
