'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET 

class Loop(Command):
    '''
    classdocs
    '''

    def __init__(self, device, start, end, step, body=None, *args, **kwargs):
        '''
        Set a device to various values in a loop, with optional check of completion and readback verification.
        @param device:     Device name
        @param start:      Initial value
        @param end:        Final value
        @param step:       Step size
        @param body:       One or more commands
        @param completion: Await __completion?
        @param readback:   False to not check any readback,
                           True to wait for readback from the 'device',
                           or name of specific device to check for readback.
        @param tolerance:  Tolerance when checking numeric readback.
                           When left as none, will default to 10% of step size.
        @param timeout:    Timeout in seconds, used for 'completion' and 'readback' check
        @param errhandler: Error handler

        Examples:
        
        # Set pv1 to 1, 1.5, 2, 2.5, 3, .., 9.5, 10
        Loop('pv1', 1, 10, 0.5)

        # Set pv1 to 10, 9, 8, 7, .., 1
        Loop('pv1', 10, 1, -1)

        Loop('pv1', 1, 10, Set('daq', 1), Delay(10), Set('daq', 0))
        Loop('pv1', 1, 10, Set('daq', 1), Delay(10), Set('daq', 0), readback=True)
        
        # Note special behavior of nested loops.
        # If step size is 'wrong', the loops will cycle direction:
        Loop('x', 1, 3, body=[ Loop('y', 1, 3, -1 ])
        # will result in these values:
        #
        # x  y
        # 1  1
        # 1  2
        # 1  3
        # 2  3
        # 2  2
        # 2  1
        # 3  1
        # 3  2
        # 3  3
        #
        # Note how the direction of the inner loop changes.
        # This can be useful for scanning the X/Y surface of a sample
        '''
        self.__device = device
        self.__start = start
        self.__end = end
        self.__step = step

        if isinstance(body, Command):
            self.__body = [ body ]
        elif body:
            self.__body = list(body)
        else:
            self.__body = list()
        if args:
            self.__body += args        
        self.__completion = kwargs['completion'] if 'completion' in kwargs else False
        self.__readback = kwargs['readback'] if 'readback' in kwargs else False
        self.__tolerance = kwargs['tolerance'] if 'tolerance' in kwargs else 0.1 * abs(step)
        self.__timeout = kwargs['timeout'] if 'timeout' in kwargs else 0
        self.__errHandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('loop')
        
        ET.SubElement(xml, 'device').text = self.__device
        ET.SubElement(xml, 'start').text = str(self.__start)
        ET.SubElement(xml, 'end').text = str(self.__end)
        ET.SubElement(xml, 'step').text = str(self.__step)
        
        need_timeout = False
        if self.__completion:
            ET.SubElement(xml, 'completion').text = 'true'
            need_timeout = True
        
        if self.__readback:
            ET.SubElement(xml, "wait").text = "true"
            ET.SubElement(xml, "readback").text = self.__device if self.__readback == True else self.__readback
            ET.SubElement(xml, "tolerance").text = str(self.__tolerance)
            need_timeout = True
        if need_timeout  and  self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)
               
        body = ET.SubElement(xml,'body')
        for command in self.__body:
            body.append(command.genXML())
            
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                          
        return xml
    
    def __repr__(self):
        return self.toCmdString()
        
    def toCmdString(self):
        result = "Loop('%s', %g, %g, %g" % (self.__device, self.__start, self.__end, self.__step)
        use_timeout = False
        if self.__completion:
            use_timeout = True
            result += ', completion=True'
        
        if len(self.__body)!=0:
            result += ", [ "
            result += ", ".join([ cmd.toCmdString() for cmd in self.__body ])
            result+= " ]"

        if self.__readback:
            use_timeout = True
            if self.__readback == True:
                result += ", readback=True"
            else:
                result += ", readback='%s'" % self.__readback
            if self.__tolerance > 0:
                result += ', tolerance=%g' % self.__tolerance
        if use_timeout  and self.__timeout > 0:
            result += ', timeout=%g' % self.__timeout
        result += ')'
        return result
