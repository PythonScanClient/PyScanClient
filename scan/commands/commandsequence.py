'''
Created on Mar 8 ,2015

@author: qiuyx
'''
import xml.etree.ElementTree as ET

from scan.commands.command import Command
from scan.util.xml import indent

class CommandSequence(object):
    """A sequence of scan commands
    
    Basically a list of commands,
    with helper methods to pretty-print
    and convert to the raw XML required by the scan server.
    
    :param commands: One or more commands, or existing list of commands.
    """
    def __init__(self, *commands):
        self.commands=[]
        for command in commands:
            # Append individual command
            if isinstance(command, Command):
                self.commands.append(command)
            else:
                # Assume iterable tuple, list, set, .. and append its content
                self.commands += list(command)
            
    def __len__(self):
        """:return: Number of commands"""
        return len(self.commands)
    
    def append(self, *commands):
        """Append more commands to the sequence
        
        :param commands: One or more commands, or existing list of commands.
        """
        for command in commands:
            # Append individual command
            if isinstance(command, Command):
                self.commands.append(command)
            else:
                # Assume iterable tuple, list, set, .. and append its content
                self.commands += list(command)
    
    def genSCN(self):
        """:return: Command in XML format suitable for scan server"""
        scn = ET.Element('commands')
        for c in self.commands:
            scn.append(c.genXML())
        
        indent(scn)
        return ET.tostring(scn)
    
    def toSeqString(self):
        """Format for printing
        
        Example:
            >>> cmds = CommandSequence(Comment('Example'), Loop('pos', 1, 5, 0.5, Set('run', 1), Delay(2), Set('run', 0)))
            >>> print cmds.toSeqString()
            
        Output::
        
            [
              Comment('Example'),
              Loop('pos', 1, 5, 0.5, [ Set('run', 1), Delay(2), Set('run', 0) ])
            ]
            
        """
        if len(self.commands) == 0:
            return "[]"
        return "[\n  " + ",\n  ".join([ cmd.toCmdString() for cmd in self.commands ]) + "\n]";
    
    def __repr__(self):
        return "CommandSequence(" + str(self.commands) + ")"
