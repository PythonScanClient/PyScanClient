'''
Parallel Command

@author: Kay Kasemir
'''
from scan.commands import Command
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class Sequence(Command):
    """Perform sequence of commands.
    
    Can be used to assemble 'meta commands' which consist
    of several basic commands.
    
    :param body:       Commands or list of commands
    :param errhandler: Optional error handler.
    
    Examples:
    
    Do nothing::
        >>> cmd = Sequence()
    
    Perform one command, same as directly using `Set('x', 1)`:
        >>> cmd = Sequence(Set('x', 1))
    
    Set two PVs to a value:
        >>> cmd = Sequence( Set('x', 1), Set('y', 2) )
    
    Becomes more useful in combination with :class:`~scan.commands.parallel.Parallel`.
    
    This example performs two sequences in parallel:
        >>> Parallel( Sequence(Set('x', 1), Wait('x_loc', 10) ),
        >>>           Sequence(Set('y', 2), Wait('y_loc', 20) )  )
    
    Nested Sequences are flattened:
        >>> # Results in the same sequence
        >>> cmd = Sequence( Sequence(Comment("One"), Comment("Two")), Comment("Three"))
        >>> cmd = Sequence( Comment("One"), Comment("Two"), Comment("Three"))
    
    """
    def __init__(self, body=None, *args, **kwargs):
        self.__body = list()
        if body:
            self.append(body)
        if args:
            self.append(*args)
        self.__errHandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
        
    def append(self, *commands):
        for cmd in commands:
            if isinstance(cmd, Sequence):
                self.append(*cmd.__body)
            else:
                self.__body.append(cmd)
        
    def genXML(self):
        xml = ET.Element('sequence')
        
        if len(self.__body)!=0:
            body = ET.SubElement(xml,'body')
            for cmd in self.__body:
                body.append(cmd.genXML())
                
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                          
        return xml
    
    def __repr__(self):
        result = 'Sequence('
        result += ", ".join([ cmd.__repr__() for cmd in self.__body ])
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result
    
    def format(self, level=0):
        result = self.indent(level) + 'Sequence(\n'
        result += ",\n".join([ cmd.format(level+1) for cmd in self.__body ])
        result += "\n" + self.indent(level) 
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result

