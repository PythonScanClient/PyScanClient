'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET

class Script(Command):
    '''
    classdocs
    '''


    def __init__(self, path='the_script.py',errHandler=None,*args):
        '''
        Constructor
        '''
        self.__path=path
        self.__args=[]
        for arg in args:
            self.__args.append(arg)
        self.__errHandler=errHandler
        
    def genXML(self):
        xml = ET.Element('script')
        ET.SubElement(xml, 'path').text = self.__path

        argLst = ET.SubElement(xml, 'arguments')
        if len(self.__args)!=0:
            for arg in self.__args:
                ET.SubElement(argLst,'argument').text = str(arg)
        
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                
        return xml
    
    def __repr__(self):
        result= 'Script( Path='+self.__path
        if len(self.__args)!=0:
            result+=', '
            for i in range(0,len(self.__args)):
                result+='Argument='+str(self.__args[i])
                if i!=len(self.__args):
                    result+=', '
        result+=')'
        return result
        
    def toCmdString(self):
        result= 'Script(Path='+self.__path
        if len(self.__args)!=0:
            result+=','
            for i in range(0,len(self.__args)):
                result+='Argument='+str(self.__args[i])
                if i!=len(self.__args):
                    result+=','
        result+=')'
        return result