'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command

class Log(Command):
    '''
    classdocs
    '''


    def __init__(self, *devices):
        '''
        Constructor
        '''
        self.devices=[]
        for device in devices:
            self.devices.append(device)
        
    def genXML(self):
        result = '<log>'
        if len(self.devices)==0:
            result+='<devices/>'
        else:
            result +='<devices>'
            for i in range(0,len(self.devices)):
                result +='<device>'+self.devices[i]+'</device>'
            result +='</devices>'    
        result += '</log>'
        return result
    
    def __str__(self):
        result = 'Log( '
        for i in range(0,len(self.devices)):
            result +='device='+self.devices[i]
            if i!=len(self.devices)-1:
                result+=', '
        result += ')'
        return result
    
    def toCmdString(self):
        result = 'Log('
        for i in range(0,len(self.devices)):
            result +='device='+self.devices[i]
            if i!=len(self.devices)-1:
                result+=', '
        result += ')'
        return result