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
    :param value_start: Initial position 
    :param value_end: Final position, inclusive
    :param value_step: Step size 
    :param condition_device: What to wait for: "seconds", pcharge device, beam monitor device
    :param condition_value: Value that condition_device should reach
    :param log: device to log, usually some neutron counts
    :param find_command: Script command to call to locate peak
    :param normalize: Normalize logged values by condition?
    :param prefix: Prefix of PVs used for results
    :param pre:          Command or list of commands executed at the start of scan.
    :param post:         Command or list of commands executed at the end of the scan.
    :param start:        Command or list of commands executed to start each step.
    :param stop:         Command or list of commands executed at the end of each step.
    :param log_always:   Optional list of device names that should be logged.    
    """
    def __init__(self, device, value_start, value_end, value_step,
                 condition_device, condition_value,
                 log,
                 find_command=None,
                 normalize=False,
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
        self.normalize = normalize
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
            if self.normalize:
                norm_device = self.condition_device
                norm_value = str(self.condition_value)
            
        if self.stop:
            loop_body += self.stop
            
        loop_body += Log(list(devices)),
        loop_body.append(Script('WriteDataToPV', [ self.device, '%s:Data:X' % self.prefix ]))
        loop_body.append(Script('WriteDataToPV', [ self.log,    '%s:Data:Y' % self.prefix, norm_device, norm_value ]))

        commands = []
        commands.append(SettingsBasedSet('%s:Height' % self.prefix, 0))
        if self.pre:
            commands += self.pre
        commands.append(SettingsBasedLoop(self.device, self.value_start, self.value_end, self.value_step, loop_body))
        if self.post:
            commands += self.post
    
        if self.find_command:
            commands.append(Script(self.find_command,
                                   [ self.device, self.log, norm_device, norm_value,
                                     '%s:Pos'    % self.prefix,
                                     '%s:Height' % self.prefix,
                                     '%s:Width'  % self.prefix
                                   ]))
        
        return commands
