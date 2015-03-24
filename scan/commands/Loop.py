'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET 

class Loop(Command):
    '''
    classdocs
    '''

    def __init__(self, device=None,start=0.0,end=10.0,step=1.0,completion=True,readback=False,wait=True,tolerance=0.1,timeout=0.2,body=[],errHandler=None):
        '''
        Constructor
        '''
        self.__device = device
        self.__start = start
        self.__end = end
        self.__step = step
        self.__completion = completion
        self.__readback = readback
        self.__wait = wait
        self.__tolerance = tolerance
        self.__timeout = timeout
        self.__body = body
        self.__errHandler = errHandler
        
    def genXML(self):
        xml = ET.Element('loop')
        
        if self.__device==None:
            ET.SubElement(xml, 'device')
        else:    
            ET.SubElement(xml, 'device').text = self.__device
            
        ET.SubElement(xml, 'start').text = str(self.__start)
        
        ET.SubElement(xml, 'end').text = str(self.__end)
        
        ET.SubElement(xml, 'step').text = str(self.__step)
        
        if self.__completion:
            ET.SubElement(xml, 'completion').text = str(self.__completion)
        
        if isinstance(self.__readback, str):
            ET.SubElement(xml, 'readback').text = str(self.__readback)
        elif self.__readback==True:
            ET.SubElement(xml, 'readback').text = self.__device

        if self.__wait==False:
            ET.SubElement(xml, 'wait').text = 'False'
            
        ET.SubElement(xml, 'tolerance').text = str(self.__tolerance)
        
        ET.SubElement(xml, 'timeout').text = str(self.__timeout)
        
        body = ET.SubElement(xml,'body')
        
        if len(self.__body)!=0:
            for command in self.__body:
                body.append(command.genXML())
                
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                          
        return xml
    
    def __repr__(self):
        result='Loop( '
        result+= 'device='+self.__device+', '
        result+= 'start='+str(self.__start)+', '
        result+= 'end='+str(self.__end)+', '
        result+= 'step='+str(self.__step)+', '
        result+= 'completion'+str(self.__completion)+', '
        result+= 'wait'+str(self.__wait)+', '
        result+= 'tolerance'+str(self.__tolerance)+', '
        if len(self.__body)!=0:
            result+= '\n[\n'
            for command in self.__body:
                result+=command.toCmdString()+',\n'
            result+= ']\n'
        result+= 'timeout'+str(self.__timeout)
        result+=')'
        return result
        
    def toCmdString(self):
        result='Loop('
        result+= 'device='+self.__device+','
        result+= 'start='+str(self.__start)+','
        result+= 'end='+str(self.__end)+','
        result+= 'step='+str(self.__step)+','
        result+= 'completion'+str(self.__completion)+','
        result+= 'wait'+str(self.__wait)+','
        result+= 'tolerance'+str(self.__tolerance)+','
        if len(self.__body)!=0:
            result+= '\n[\n'
            for command in self.__body:
                result+=command.toCmdString()+',\n'
            result+= ']\n'
        result+= 'timeout'+str(self.__timeout)
        result+=')'
        return result