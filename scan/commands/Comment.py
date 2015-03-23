'''
Created on Mar 8,2015

@author: qiuyx
'''
from scan.commands.Command import Command

class Comment(Command):
    '''
    Comment Class.
    SubClass of py.
    '''
    
    def __init__(self, comment="This is an example comment."):
        '''
        params comment Comments needed to add.
        '''
        self.comment=comment
    
    def genXML(self):
        return '<comment>'+'<text>'+self.comment+'</text>'+'</comment>'

    def __repr__(self):
        return 'Comment(Comment='+self.comment+')'
    
    def toCmdString(self):
        '''
        Give a printing of this Command. 
        '''
        return 'Comment(Comment='+self.comment+')'
    
    
        