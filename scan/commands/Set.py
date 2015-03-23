'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command

class Set(Command):
    '''
    classdocs
    '''


    def __init__(self, device=None,value=0.0,completion=False,wait=True,tolerance=0.1,timeOut=0.0):
        '''
        Constructor
        '''
        self.device=device
        self.value=value
        self.completion=completion
        self.wait=wait
        self.tolerance=tolerance
        self.timeOut=timeOut
        
    def genXML(self):
        result= '<set>'
        if self.device==None:
            result+='<device/>'
        else:
            result+='<device>'+self.device+'</device>'
        result+='<value>'+str(self.value)+'</value>'
        if self.completion==True:
            result+='<completion>true</completion>'
        if self.wait==False:
            result+='<wait>false</wait>'
        result+='<tolerance>'+str(self.tolerance)+'</tolerance>'
        if self.timeOut!=0.0:
            result+='<timeout>'+str(self.timeOut)+'</timeout>'
        result+='</set>'
        
        return result
    
    def __str__(self):
        result= 'Set( device='+self.device
        result+= ', value='+str(self.value)
        if self.completion==True:
            result+=', completion=true'
        if self.wait==False:
            result+=', wait=false'
        if self.timeOut!=0.0:
            result+=', timeOut='+str(self.timeOut)
        result+=')'
        return result
    
    def toCmdString(self):
        result= 'Set(device='+self.device
        result+= ',value='+str(self.value)
        if self.completion==True:
            result+=',completion=true'
        if self.wait==False:
            result+=',wait=false'
        if self.timeOut!=0.0:
            result+=',timeOut='+str(self.timeOut)
        result+=')'
        return result
    
        