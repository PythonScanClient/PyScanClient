"""
Helper for assembling a range or 'alignment' scan
:author: Kay Kasemir
"""
from scan.commands.command import Command
from scan.commands.delay import Delay
from scan.commands.log import Log
from scan.commands.script import Script
from scan.util.scan_settings import SettingsBasedSet, SettingsBasedLoop, SettingsBasedWait

class AlignmentScan(object):
    """Assemble commands for 'alignment' scan.
    
    :param device: Device to move 
    :param start: Initial position 
    :param end: Final position, inclusive
    :param step: Step size 
    :param run_per_step: Create one run per step? Otherwise one big run with SMS step markers
    :param condition_device: What to wait for: "seconds", pcharge device, beam monitor device
    :param condition_value: Value that condition_device should reach
    :param log: device to log, usually some neutron counts
    :param method: "None", "Edge", "Gauss+const", "Gauss+slope"
    
    :return: ( commands, name )
    
    This example will move the '..Angle' from 0 to 90 degrees in steps of 2 within one 'run'.
    At each step it will wait for 1e12 PCharge, then log the neutron counts.
    Finally, the neutron counts at each step will be normalized by (actual_pcharge_at_step / 1e12),
    and a gauss with constant baseline will be fit.

    Example::
        ( commands, name ) = createAlignmentScan(
                        'BL99:Mot:Angle', 0, 90, 2, run_per_step=False,
                        'BL99:PCharge', 1e12,
                        'BL99:Det:Neutrons')
        id = scan_client.submit(commands, name)
        
        scan_client.waitUntilDone(id)
        data = scan_client.getData(id)
        table = createTable(data, 'BL99:Mot:Angle', 'BL99:Det:Neutrons')
        x = np.array(table[0])
        y = np.array(table[1])
    """

    def __init__(self, device, value_start, value_end, value_step,
                 condition_device, condition_value,
                 log,
                 find_command=None,
                 prefix = 'Demo:CS:Scan:Fit',
                 pre=None, post=None, start=None, stop=None,
                 log_always=[]):
        self.device = device
        self.value_start = value_start
        self.value_end = value_end
        self.value_step = value_step
        self.condition_device = condition_device
        self.condition_value = condition_value
        self.log = log
        self.find_command = find_command
        self.prefix = prefix
        self.pre = self.__makeList(pre)
        self.post = self.__makeList(post)
        self.start = self.__makeList(start)
        self.stop = self.__makeList(stop)
        self.log_always=log_always


    def __makeList(self, cmd):
        if isinstance(cmd, Command):
            return [ cmd ]
        if cmd:
            return list(cmd)
        return None


    def createScan(self):
        """Create scan.
        
        :return: List of commands.
        """
 
        # Assemble commands from 'inside' out, starting with the innermost wait and log
    
        # Older scan ScriptCommand didn't allow empty arguments, so use "-"
        norm_device = "-"
        norm_value = "1"
        
        devices = set(self.log_always)
        devices.add(self.device)
        devices.add(self.log)
        
          
        # Assemble commands for loop body
        loop_body = []
        if self.start:
            loop_body += self.start
            
        if self.condition_device == "seconds":
            loop_body.append(Delay(self.condition_value))
        else:
            loop_body.append(SettingsBasedWait(self.condition_device, self.condition_value))
            devices.add(self.condition_device)
            
        if self.stop:
            loop_body += self.stop
            
        loop_body += Log(list(devices)),
        loop_body.append(Script('WriteDataToPV', [ self.device, '%s:Data:X' % self.prefix ]))
        loop_body.append(Script('WriteDataToPV', [ self.log,    '%s:Data:Y' % self.prefix, norm_device, norm_value ]))


        commands = []
        if self.pre:
            commands += self.pre
        commands.append(SettingsBasedLoop(self.device, self.value_start, self.value_end, self.value_step, loop_body))
        if self.post:
            commands += self.post
    
        if self.find_command:
            commands.insert(0, Set('%s:CS:Scan:Fit:Height' % scan_settings.S, 0))
            commands.append(Script(find_command,
                                   [ self.device, self.log, 
                                     '%s:CS:Scan:Fit:Pos'    % scan_settings.S,
                                     '%s:CS:Scan:Fit:Height' % scan_settings.S,
                                     '%s:CS:Scan:Fit:Width'  % scan_settings.S
                                   ]))
        
        return commands
    
    

