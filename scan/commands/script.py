'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.command import Command
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

class Script(Command):
    """Custom command implemented in Jython
    
    This command executes Jython code.
    
    :param script: Name of the script class.
    :param arguments...: Arguments to the script.
    
    Example Script:
    
    Scripts must derive from `ScanScript`:
    
    >>> class MyScript(ScanScript):
    ...    # Script command that gets logged data for a PV,
    ...    # writes the sum to a '.._sum' PV
    ...    def __init__(self, name):
    ...        self.name = name
    ...
    ...    def getDeviceNames(self):
    ...        # PVs that this command needs
    ...        return [ self.name + "_sum" ]
    ...
    ...    def run(self, context, args):
    ...        [ x ] = context.getData(self.name)
    ...        s = 0
    ...        for v in x:
    ...            s += v
    ...        context.write(self.name + "_sum", s)
    
    For details refer to the Javadoc of the Scan Server.
    
    A Jython script that defines the class `MyScript` must
    be stored in file named `myscript.py`,
    i.e. using the lower case version of the class name.
    It must be located on the scan server script path.

    Example Script commands:
        >>> cmd = Script("MyScript", "pos", 42.3)
    """
    def __init__(self, script='the_script.py', *args, **kwargs):
        self.__path = script
        # If args[0] is already a list, use that
        if len(args) == 1  and  len(args[0]) > 0:
            self.__args = args[0]
        else:
            self.__args = args
        self.__errHandler = kwargs['errHandler'] if 'errHandler' in kwargs else None
        
    def genXML(self):
        xml = ET.Element('script')
        ET.SubElement(xml, 'path').text = self.__path

        if len(self.__args)!=0:
            argLst = ET.SubElement(xml, 'arguments')
            for arg in self.__args:
                ET.SubElement(argLst,'argument').text = str(arg)
        
        if self.__errHandler:
            ET.SubElement(xml,'error_handler').text = str(self.__errHandler)
                
        return xml
    
    def __repr__(self):
        result= "Script('%s'" % self.__path
        for arg in self.__args:
            if isinstance(arg, str):
                result += ", '%s'" % arg
            else:
                result += ", " + str(arg)
        if self.__errHandler:
            result += ", errhandler='%s'" % self.__errHandler
        result+=')'
        return result
