'''
Created on Mar 8,2015
@author: qiuyx
'''
from abc import abstractmethod

class Command(object):
    '''
    Abstract father Command Class.
    Sub Command must implement generalize() method.
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @abstractmethod
    def genXML(self):
        pass
    
    @abstractmethod
    def toCmdString(self):
        pass