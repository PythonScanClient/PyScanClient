'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command

class Script(Command):
    '''
    classdocs
    '''


    def __init__(self, path='the_script.py',*args):
        '''
        Constructor
        '''
        self.path=path
        self.args=[]
        for arg in args:
            self.args.append(arg)
     
    def genXML(self):
        result= '<script><path>'+self.path+'</path>'
        if len(self.args)!=0:
            result+='<arguments>'
            for arg in self.args:
                result+='<argument>'+str(arg)+'</argument>'
            result+='</arguments>'
        else:
            result+='<arguments/>'
        result+='</script>'
        return result
    
    def __str__(self):
        result= 'Script( Path='+self.path
        if len(self.args)!=0:
            result+=', '
            for i in range(0,len(self.args)):
                result+='Argument='+str(self.args[i])
                if i!=len(self.args):
                    result+=', '
        result+=')'
        return result
        
    def toCmdString(self):
        result= 'Script(Path='+self.path
        if len(self.args)!=0:
            result+=','
            for i in range(0,len(self.args)):
                result+='Argument='+str(self.args[i])
                if i!=len(self.args):
                    result+=','
        result+=')'
        return result