'''
Created on Mar 8 ,2015

@author: qiuyx
'''
import xml.etree.ElementTree as ET

class CommandSequence(object):
    '''
    A Sequence is a list of all the ordered commands of a scan.
    Sequence is used to manually build a scan in a visualized 
    Python command-line or script.Each Sequence is an instance,
    such that mutiple sequences can be built for submitting in 
    the ScanServerClient Side.
    '''


    def __init__(self, *Commands):
        '''
        Constructor
        '''
        self.commands=[]
        self.cnt = 0
        for command in Commands:
            self.commands.append(command)
            self.cnt+=1
    
    def genSCN(self):
        '''
        Get the .SCN file content of this Sequence.
        '''
        scn = ET.Element('commands')
        for c in self.commands:
            scn.append(c.genXML())
        
        return ET.tostring(scn)
    
    def toSeqString(self):
        '''
        Show the contents of this Sequence.
        
        Example:
        >>> cmds = CmdSeq(
                       CommentCommand(comment='haha'),
                       CommentCommand('hehe'),
                       LoopCommand(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
                                   body=[CommentCommand(comment='haha'),
                                         ConfigLogCommand(automatic=True)
                                         ]),
                       ScriptCommand('submit.py',1,'abc',0.05)
                    )
        >>> print cmds.toSeqString()
        Output is:
        >>> [
                CommentCommand(comment='haha'),
                CommentCommand('hehe'),
                LoopCommand(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
                            body=[CommentCommand(comment='haha'),
                                  ConfigLogCommand(automatic=True)
                                 ]),
                ScriptCommand('submit.py',1,'abc',0.05)
            ]
        '''
        
        result ='['
        if self.cnt!=0:
            result+='\n'
        for i in range(0,self.cnt):
            result += self.commands[i].toCmdString()
            if i!=self.cnt-1:
                result+=', '
            result +='\n'
        result+=']'
        return result