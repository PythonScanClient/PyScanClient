'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command

class Loop(Command):
    '''
    classdocs
    '''

    def __init__(self, device=None,start=0.0,end=10.0,step=1.0,completion=True,wait=True,tolerance=0.1,timeOut=0.2,body=[]):
        '''
        Constructor
        '''
        self.device=device
        self.start=start
        self.end=end
        self.step=step
        self.completion=completion
        self.wait=wait
        self.tolerance=tolerance
        self.timeOut=timeOut
        self.body=body
    
    def genXML(self):
        result= '<loop>'
        if self.device==None:
            result+='<device/>'
        else:    
            result+='<device>'+self.device+'</device>'
        result+='<start>'+str(self.start)+'</start>'
        result+='<end>'+str(self.end)+'</end>'
        result+='<step>'+str(self.step)+'</step>'
        if self.completion:
            result+='<completion>'+str(self.completion)+'</completion>'
        if self.wait==False:
            result+='<wait>'+str(self.wait)+'</wait>'
        result+='<tolerance>'+str(self.tolerance)+'</tolerance>'
        result+='<timeout>'+str(self.timeOut)+'</timeout>'
        if len(self.body)!=0:
            result+='<body>'
            for command in self.body:
                result+=command.genXML()
            result+='</body>'
        result+='</loop>'
        return result
    
    def __str__(self):
        result='Loop( '
        result+= 'device='+self.device+', '
        result+= 'start='+str(self.start)+', '
        result+= 'end='+str(self.end)+', '
        result+= 'step='+str(self.step)+', '
        result+= 'completion'+str(self.completion)+', '
        result+= 'wait'+str(self.wait)+', '
        result+= 'tolerance'+str(self.tolerance)+', '
        if len(self.body)!=0:
            result+= '\n[\n'
            for command in self.body:
                result+=command.toCmdString()+',\n'
            result+= ']\n'
        result+= 'timeout'+str(self.timeOut)
        result+=')'
        return result
        
    def toCmdString(self):
        result='Loop('
        result+= 'device='+self.device+','
        result+= 'start='+str(self.start)+','
        result+= 'end='+str(self.end)+','
        result+= 'step='+str(self.step)+','
        result+= 'completion'+str(self.completion)+','
        result+= 'wait'+str(self.wait)+','
        result+= 'tolerance'+str(self.tolerance)+','
        if len(self.body)!=0:
            result+= '\n[\n'
            for command in self.body:
                result+=command.toCmdString()+',\n'
            result+= ']\n'
        result+= 'timeout'+str(self.timeOut)
        result+=')'
        return result