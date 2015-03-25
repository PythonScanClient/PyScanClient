'''
Created on Mar 8,2015
@author: qiuyx
'''
from abc import abstractmethod

class Command(object):
    """Base class for all commands."""
    
    @abstractmethod
    def genXML(self):
        """:return: XML representation of the command."""
        pass

    @abstractmethod
    def __repr__(self):
        """:return: Representation that can be used to create the command in python."""
        return "Command()"
    
    def toCmdString(self):
        """By default, calls `__repr__()`.
        :return: Human-readable, concise representation.
        """
        return self.__repr__()