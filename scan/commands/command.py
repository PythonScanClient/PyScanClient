'''
Created on Mar 8,2015
@author: qiuyx
'''
from abc import abstractmethod, ABCMeta

# Metaclass compatible with Python 2 *and* 3
# (See: https://stackoverflow.com/questions/35673474/using-abc-abcmeta-in-a-way-it-is-compatible-both-with-python-2-7-and-python-3-5)
ABC = ABCMeta('ABC', (object,), {'__slots__': ()}) 

class Command(ABC):
    """Base class for all commands."""
    
    @abstractmethod
    def genXML(self):
        """:return: XML representation of the command."""
        pass

    @abstractmethod
    def __repr__(self):
        """:return: Representation that can be used to create the command in python."""
        return "Command()"

    def __str__(self):
        """By default, calls `__repr__()`.
        :return: Concise, human-readable representation.
        """
        return self.__repr__()

    def indent(self, level):
        return "    " * level
    
    def format(self, level=0):
        """Format the command, possible over multiple lines.
        
        :param level: Indentation level
        
        :return: Human-readable, possibly multi-line representation.
        """
        return self.indent(level) + self.__str__()
