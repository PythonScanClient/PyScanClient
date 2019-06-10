from scan.commands.command import Command
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class If(Command):
    """Conditionally execute commands.
    
    :param device:     Device name
    :param value:      Desired value.
    :param comparison: How current value is compared to the desired value.
                       Options: '=', '>', '>=', '<' , '<='.
    :param body:       One or more commands
    :param tolerance:  Tolerance when checking numeric `readback`.
                       Defaults to 0.1
    :param errhandler: Error handler
    
    Examples:
    
        >>> cmd = If('pv1', '=', 10, [ Comment("It's 10") ])
    """

    __comparisons= {'=':'EQUALS',
                    '>':'ABOVE',
                    '>=':'AT_LEAST',
                    '<':'BELOW',
                    '<=':'AT_MOST'}

    def __init__(self, device, comparison, value, body=None, *args, **kwargs):
        if not isinstance(device, str):
            raise Exception("Expect device name, got '%s'" % str(device))
        self.__device = device

        if isinstance(body, Command):
            self.__body = [ body ]
        elif body:
            self.__body = list(body)
        else:
            self.__body = list()
        if args:
            self.__body += args
        if not comparison in If.__comparisons:
            raise Exception("Invalid comparison '%s'" % comparison)
        self.__comparison = comparison
        self.__desiredValue = value
        self.__tolerance = kwargs['tolerance'] if 'tolerance' in kwargs else 0.1
        self.__errHandler = kwargs['errhandler'] if 'errhandler' in kwargs else None
            
    def getDevice(self):
        """:return: Device name"""
        return self.__device
            
    def getBody(self):
        """Obtain list of body commands.
        
           The If(..) constructor creates a safe
           copy of the passed 'body' to prevent side effects
           when that body is later changed and maybe
           used to construct another If(..) instance.
           
           If there is a desire to change the body
           (before it's submitted to the scan server),
           this method provides that list of commands.

           :return: Body
        """
        return self.__body
        
    def genXML(self):
        xml = ET.Element('if')
        
        ET.SubElement(xml, 'device').text = self.__device
        ET.SubElement(xml, 'comparison').text = If.__comparisons[self.__comparison]
        ET.SubElement(xml, 'value').text = str(self.__desiredValue)
        ET.SubElement(xml, "tolerance").text = str(self.__tolerance)
             
        body = ET.SubElement(xml,'body')
        for command in self.__body:
            body.append(command.genXML())
            
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                          
        return xml
    
    def __repr__(self):
        result = "If('%s', '%s'" % (self.__device, self.__comparison)
        if isinstance(self.__desiredValue, str):
            result += ", '%s'" % self.__desiredValue
        else:
            result += ", %s" % str(self.__desiredValue)

        if len(self.__body)!=0:
            result += ", [ "
            result += ", ".join([ cmd.__repr__() for cmd in self.__body ])
            result+= " ]"
        result += ', tolerance=%g' % self.__tolerance
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result += ')'
        return result

    def format(self, level=0):
        result = self.indent(level) + "If('%s', '%s'" % (self.__device, self.__comparison)
        if isinstance(self.__desiredValue, str):
            result += ", '%s'" % self.__desiredValue
        else:
            result += ", %s" % str(self.__desiredValue)

        if len(self.__body)!=0:
            result += ",\n" + self.indent(level) + "[\n"
            result += ",\n".join([ cmd.format(level+1) for cmd in self.__body ])
            result += "\n" + self.indent(level) + "]"


        if self.__tolerance > 0:
            result += ', tolerance=%g' % self.__tolerance
        result += ')'
        return result
