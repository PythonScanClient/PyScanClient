'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command
import xml.etree.ElementTree as ET

class Wait(Command):
    '''
    Command that delays the scan until a device reaches a certain value.It has 6 properties in the following order:
    1.device
    2.desiredValue
    3.comparison
    4.tolerance
    5.timeout
    6.errHandler
    '''
    __comparisons= {'=':'EQUALS',
                    '>':'ABOVE',
                    '>=':'AT_LEAST',
                    '<':'BELOW',
                    '<=':'AT_MOST',
                    'to increase by':'INCREASE_BY',
                    'to decrease by':'DECREASE_BY'}

    def __init__(self, device=None,desiredValue=0.0,comparison='=',tolerance=0.1,timeout=0.0,errHandler=None):
        '''
        Wait for a device to some vaule.
        Instantiation needs 6 params in the following order:
        :param  device:             Name of PV or device. Defaults None.
        :param  desiredValue:       Value wait to. Defaults 0.0
        :param  comparison:         Comparison with the desiredValue. 
                                    Defaults '=' ,other available:
                                             '>' ,
                                             '>=',
                                             '<' ,
                                             '<=',
                                             'to increase by',
                                             'to decrease by'
                                    
        :param  tolerance:          Defaults 0.1
        :param  timeout             Defaults 0.0
        :param  errHandler          Defaults None
        
        Usage::
        >>> wcmd=Wait(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0,errHandler='someHandler')
        '''
        self.__device=device
        self.__desiredValue=desiredValue
        self.__comparison=self.__comparisons[comparison]
        self.__tolerance=tolerance
        self.__timeout=timeout
        self.__errHandler=errHandler
        
    def genXML(self):
        '''
        Generating .scn text.
        '''
        xml = ET.Element('wait')
        
        dev = ET.SubElement(xml, 'device')
        
        if self.__device != None:
            dev.text = str(self.__device)
            
        ET.SubElement(xml, 'value').text = str(self.__desiredValue)
        
        ET.SubElement(xml, 'comparison').text = self.__comparison
        
        if self.__tolerance!=0.0:
            ET.SubElement(xml,'tolerance').text = str(self.__tolerance)
            
        if self.__timeout!=0.0:
            ET.SubElement(xml,'timeout').text = str(self.__timeout)
            
        if self.__errHandler!=None:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
            
        return ET.tostring(xml)
    
    def __repr__(self):
        '''
        Overwrite the built-in __str__ method to give a pretty printing. 
        '''
        result= 'Wait( '
        result+= 'device='+str(self.__device)+', '
        result+= 'desiredValue='+str(self.__desiredValue)+', '
        result+= 'comparison='+self.__comparison+', '
        result+= 'tolerance='+str(self.__tolerance)+', '
        result+= 'timeout='+str(self.__timeout)+', '
        if self.__errHandler!=None:
            result+= 'errHandler='+self.__errHandler
        result+= ' )'
        return result

    def toCmdString(self):
        '''
        Give a printing of this Command. 
        '''
        result= 'Wait( '
        result+= 'device='+str(self.__device)+', '
        result+= 'desiredValue='+str(self.__desiredValue)+', '
        result+= 'comparison='+self.__comparison+', '
        result+= 'tolerance='+str(self.__tolerance)+', '
        result+= 'timeout='+str(self.__timeout)+', '
        if self.__errHandler!=None:
            result+= 'errHandler='+self.__errHandler
        result+= ' )'
        return result