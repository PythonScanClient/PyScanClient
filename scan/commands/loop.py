'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
import xml.etree.ElementTree as ET 

class Loop(Command):
    """Set a device to various values in a loop.
    
    Optional check of completion and readback verification.
    
    :param device:     Device name
    :param start:      Initial value
    :param end:        Final value
    :param step:       Step size
    :param body:       One or more commands
    :param completion: Await callback completion?
    :param readback:   `False` to not check any readback,
                       `True` to wait for readback from the 'device',
                       or name of specific device to check for readback.
    :param tolerance:  Tolerance when checking numeric `readback`.
                       Defaults to 0.
    :param timeout:    Timeout in seconds, used for `completion` and `readback` check.
    :param errhandler: Error handler
    
    Examples:
    
    Set `pv1` to 1, 1.5, 2, 2.5, 3, .., 9.5, 10:
        >>> cmd = Loop('pv1', 1, 10, 0.5)
    
    Set `pv1` to 10, 9, 8, 7, .., 1, i.e. stepping down:
        >>> cmd = Loop('pv1', 10, 1, -1)
    
    At each step of the loop, perform additional commands:
        >>> cmd = Loop('pv1', 1, 10, 1, Set('daq', 1), Delay(10), Set('daq', 0))
        >>> cmd = Loop('pv1', 1, 10, 1,
        ...            body = [ Set('daq', 1), Delay(10), Set('daq', 0) ])
    
    When after loop updates `pv1`, check for its readback to match, then perform commands within the loop:
        >>> cmd = Loop('pv1', 1, 10, 1, Set('daq', 1), Delay(10), Set('daq', 0), readback=True)
    
    .. _`loop-direction`:
    
    
    For nested loops, note the special handling of the step direction.
    Consider a normal nested loop for 'xpos' and 'ypos' both stepping from 0 to 5 with a positive step:
    
        >>> cmd = Loop('xpos', 0, 5, 1, [ Loop('ypos', 0, 5, 1 ])
    
    In this example, the step size for the inner loop is 'wrong'.
    Going from 0 to 5 ordinarily means stepping up by +1 in each loop iteration,
    but the step is instead provided as -1, as if this was a loop from 5 down to 0:
    
        >>> cmd = Loop('xpos', 0, 5, 1, [ Loop('ypos', 0, 5, -1 ])
    
    As a result, the loop will cycle its direction between +1 and -1.
    
    .. image:: scan_alternate.png
    
    Note how the direction of the inner loop changes.
    This can be useful for scanning the X/Y surface of a sample.    
    
    """
    def __init__(self, device, start, end, step, body=None, *args, **kwargs):
        if not isinstance(device, str):
            raise Exception("Expect device name, got '%s'" % str(device))
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
        self.__tolerance = kwargs['tolerance'] if 'tolerance' in kwargs else abs(step)/10.0
        self.__timeout = kwargs['timeout'] if 'timeout' in kwargs else 0
        self.__errHandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
            
    def getDevice(self):
        """:return: Device name"""
        return self.__device
            
    def setCompletion(self, completion):
        """Change completion
        
        :param completion: Await callback completion?
        """
        self.__completion = completion

    def setReadback(self, readback):
        """Change readback
        
        :param readback: `False` to not check any readback,
               `True` to wait for readback from the `device`,
               or name of specific device to check for readback.
        """
        self.__readback = readback

    def setTolerance(self, tolerance):
        """Change tolerance
        
        :param tolerance:  Tolerance when checking numeric `readback`.
        """
        self.__tolerance = tolerance

    def setTimeout(self, timeout):
        """Change timeout
        
        :param timeout:    Timeout in seconds, used for `completion` and `readback`.
        """
        self.__timeout = timeout
        
    def getBody(self):
        """Obtain list of body commands.
        
           The Loop(..) constructor creates a safe
           copy of the passed 'body' to prevent side effects
           when that body is later changed and maybe
           used to construct another Loop(..) instance.
           
           If there is a desire to change the loop's body
           (before it's submitted to the scan server),
           this method provides that list of commands.
           :return: Loop body
        """
        return self.__body
        
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
        else:
            ET.SubElement(xml, "wait").text = "false"
        if need_timeout  and  self.__timeout > 0:
            ET.SubElement(xml, "timeout").text = str(self.__timeout)
               
        body = ET.SubElement(xml,'body')
        for command in self.__body:
            body.append(command.genXML())
            
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                          
        return xml
    
    def __repr__(self):
        result = "Loop('%s', %g, %g, %g" % (self.__device, self.__start, self.__end, self.__step)
        use_timeout = False
        if len(self.__body)!=0:
            result += ", [ "
            result += ", ".join([ cmd.__repr__() for cmd in self.__body ])
            result+= " ]"
        if self.__completion:
            use_timeout = True
            result += ', completion=True'        
        if self.__readback:
            use_timeout = True
            if self.__readback == True:
                result += ", readback=True"
            else:
                result += ", readback='%s'" % self.__readback
            if self.__tolerance is not None:
                result += ', tolerance=%g' % self.__tolerance
        if use_timeout  and self.__timeout > 0:
            result += ', timeout=%g' % self.__timeout
        result += ')'
        return result

    def format(self, level=0):
        result = self.indent(level) + "Loop('%s', %g, %g, %g" % (self.__device, self.__start, self.__end, self.__step)
        use_timeout = False
        if len(self.__body)!=0:
            result += ",\n" + self.indent(level) + "[\n"
            result += ",\n".join([ cmd.format(level+1) for cmd in self.__body ])
            result += "\n" + self.indent(level) + "]"
        if self.__completion:
            use_timeout = True
            result += ', completion=True'        
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
