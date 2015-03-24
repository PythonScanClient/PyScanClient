'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET

class Wait(Command):
    '''
    command that delays the scan until a device reaches a certain value.It has 6 properties in the following order:
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
                    'increase by':'INCREASE_BY',
                    'decrease by':'DECREASE_BY'}

    def __init__(self, device, value, comparison='=', tolerance=0.0, timeout=0.0, errhandler=None):
        '''
        Wait for a device to some vaule.
        Instantiation needs 6 params in the following order:
        :param  device:             Name of PV or device. Defaults None.
        :param  desiredValue:       Value Wait to. Defaults 0.0
        :param  comparison:         Comparison with the desiredValue. 
                                    Defaults '=' ,other available:
                                             '>' ,
                                             '>=',
                                             '<' ,
                                             '<=',
                                             'increase by',
                                             'decrease by'
                                    
        :param  tolerance:          Defaults 0.1
        :param  timeout             Defaults 0.0
        :param  errHandler          Defaults None
        
        Usage::
        >>> wcmd = Wait('shutter', 1)
        >>> wcmd = Wait('position', 25.0, timeout=60.0, tolerance=0.5)
        >>> wcmd = Wait('counts', 1e12, comparison='>=', timeout=10.0)
        >>> wcmd = Wait('counts', 1e12, comparison='increase by', timeout=5.0, errhandler='someHandler')
        '''
        self.__device=device
        self.__desiredValue=value
        if not comparison in Wait.__comparisons:
            raise Exception("Invalid comparison '%s'" % comparison)
        self.__comparison=comparison
        self.__tolerance=tolerance
        self.__timeout=timeout
        self.__errHandler=errhandler
        
    def genXML(self):
        '''
        Generating .scn text.
        '''
        xml = ET.Element('wait')
        
        ET.SubElement(xml, 'device').text = self.__device
            
        ET.SubElement(xml, 'value').text = str(self.__desiredValue)
        
        ET.SubElement(xml, 'comparison').text = Wait.__comparisons[self.__comparison]
        
        if self.__tolerance > 0.0:
            ET.SubElement(xml,'tolerance').text = str(self.__tolerance)
            
        if self.__timeout > 0.0:
            ET.SubElement(xml,'timeout').text = str(self.__timeout)
            
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = self.__errHandler
            
        return xml
    
    def __repr__(self):
        return self.toCmdString()

    def toCmdString(self):
        '''
        Give a printing of this command. 
        '''
        result = "Wait('%s'" % self.__device
        if isinstance(self.__desiredValue, str):
            result += ", '%s'" % self.__desiredValue
        else:
            result += ", %s" % str(self.__desiredValue)
        if self.__comparison != '=':
            result += ", comparison='%s'" % self.__comparison
        if self.__tolerance > 0:
            result += ', tolerance=%g' % self.__tolerance
        if self.__timeout > 0:
            result += ', timeout=%g' % self.__timeout
        if self.__errHandler!=None:
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result