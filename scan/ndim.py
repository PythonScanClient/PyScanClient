"""N-Dimensional Scan

"""
# @author Kay Kasemir

from scan.util import SettingsBasedLoop
from scan.commands.command import Command
from scan.commands.log import Log

def createNDimScan(*parameters):
    """N-dimensional scan
    
    Creates nested `Loop` commands for N-dimensional scan.
    Logs arbitrary number of reading.
    
    :param parameters: One or more parameters
    
    Parameters include:
    
    * Individual `Set`, `Wait`, ... command or list of commands
    * Loop specification `('device', start, end)`
      or `('device', start, end, step)`
      to create a loop
    * Names of device to log in addition to loop'ed devices
    
    All the devices used in loops or mentioned as device names
    will be logged in the innermost loop.
    
    Example for scanning 'xpos' from 1 to 10, stepping 1. 'xpos' will be logged::
    
    >>> cmds = createNDimScan( ('xpos', 1, 10) )
    
    Log the 'readback' together with 'xpos' from the loop::
    
    >>> cmds =  createNDimScan( ('xpos', 1, 10), 'readback')
    
    Scan 'xpos', with an inside loop for 'ypos',
    logging 'readback' in addition to 'xpos' and 'ypos'::
    
    >>> cmds =  createNDimScan( ('xpos', 1, 10), ('ypos', 1, 5, 0.2), 'readback')

    Scan 'xpos' and 'ypos', toggling something to 1 and then 0 in the inner loop::
    
    >>> cmds = createNDimScan(('xpos', 1, 10), ('ypos', 1, 5, 0.2), Set('xyz', 1), Set('xyz', 0))
    """
    # Turn args into modifiable list
    args = list(parameters)

    # Assemble the commands
    return __decodeScan(set(), args)
 
def __decodeLoop(parms):
    """Decode loop parameters
    
    :param parms: ('device', start, end, step) or ('device', start, end)
    :return: ('device', start, end, step)
    """
    if (len(parms) == 4):
        return (parms[0], parms[1], parms[2], parms[3])
    elif (len(parms) == 3):
        return (parms[0], parms[1], parms[2], 1)
    else:
        raise Exception('Scan parameters should be (''device'', start, end, step), not %s' % str(parms))
    
def __decodeScan(to_log, args):
    """
    Recursively build commands from scan arguments
    :param to_log: Devices to log
    :param args: Remaining scan arguments 
    :return: List of commands
    """
    if len(args) <= 0:
        # Reached innermost layer, no arguments left.
        # Log what needs to be logged. May be nothing.
        if len(to_log) <= 0:
            return []
        return [ Log(list(to_log)) ]
    
    # Analyze next argument
    arg = args.pop(0)
    if isinstance(arg, str):
        # Remember device to log
        to_log.add(arg)
        return __decodeScan(to_log, args)
    elif isinstance(arg, tuple):
        # Loop specification
        scan = __decodeLoop(arg)
        # Remember loop variable for log
        # not log local variable
        if not scan[0].lower().startswith('loc://'):
            to_log.add(scan[0])
        # Create loop with remaining arguments as body
        return [ SettingsBasedLoop(scan[0], scan[1], scan[2], scan[3],
                                   __decodeScan(to_log, args))
               ]
    elif isinstance(arg, list):
        for cmd in arg:
            if not isinstance(cmd, Command):
                raise Exception("Expected list of commands, got %s" % str(arg))
        cmds = arg
        cmds.extend(__decodeScan(to_log, args))
        return cmds
    elif isinstance(arg, Command):
        # Create list of commands
        cmds = [ arg ]
        cmds.extend(__decodeScan(to_log, args))
        return cmds
    else:
        raise Exception('Cannot handle scan parameter of type %s' % arg.__class__.__name__)

