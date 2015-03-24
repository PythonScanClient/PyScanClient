'''
Created on 2014-1-12
@author: qiuyx
'''
from __builtin__ import str
'''
from Scan import ScanClient
from Scan.Command import Command
from Scan.CmdSequence import CmdSequence
from Scan.Comment import Comment
from Scan.Include import Include
from Scan.Script import Script
from Scan.Wait import Wait
from Scan.Delay import Delay
from Scan.Log import Log
from Scan.Loop import Loop
from Scan.Set import Set
from Scan.ConfigLog import ConfigLog
'''
from scan import *

#get the client instance
sc = ScanClient('localhost','4810')

####################2015-3-8 New ScanClient####################
#generalize client instance:
sc = ScanClient(host='localhost',port=4810)

cc = Comment(text='haha')
#Create Command Sequence:

cmds1 = CmdSequence(
   Comment(text='haha'),
   Comment('hehe'),
   ConfigLog(auto=True),
   Delay(seconds=2.0),
   Include(scanFile='1.scn',macros='macro=value'),
   Log(None,'shutter','xpos','ypos'),
   Loop(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,readback=True,
               body=[
                     ConfigLog(auto=True),Comment(text='haha')
                     ]),
   Script('submit.py',1,'abc',0.05),
   Set(device='shutter',value=0.1,completion=True,tolerance=0.1,timeout=0.1,readback='pcharge'),
   Wait(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
)
cmds2=[
       cc,
       Comment('hehe'),
       ConfigLog(auto=True),
       Delay(seconds=2.0),
       Include(scanFile='1.scn',macros='macro=value'),
       Log('shutter','xpos','ypos'),
       Loop(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
               body=[Comment(text='haha'),
                     ConfigLog(auto=True)
                     ]),
       Script('submit.py',1,'abc',0.05),
       Set(device='shutter',value=0.1,completion=True,tolerance=0.1,timeout=0.1),
       Wait(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
      ]

#print cc
#print 'cmds2:------',cmds2
print cmds1.genSCN() 
print sc.genSCN4List(cmds2)

#submit XML:
sc.submit(cmds1.genSCN(),'TestSubmitXML')
#submit CmdSequence:
sc.submit(cmds1,'TestSubmitSeq')
#submit List

#sc.submit(cmds2,'TestSubmitList')
'''
#print c.toCmdString()
print sc.genSCN4List(cmds2)
#have a look at the sequence:
print 'cmds1=',cmds1.toSeqString()
print 'cmds2=',str(cmds2)
#have a look at the generated .scn file:
print cmds1.genSCN()

#submit XML:
sc.submit(cmds1.genSCN(),'TestSubmitXML')
#submit CmdSequence:
sc.submit(cmds1,'TestSubmitSeq')
#submit List
sc.submit(cmds2,'TestSubmitList')
'''


'''
for i in range(278,283):
    sc.abort(i)
else:
    print 'All scans aborted.'
'''
#check scan server
print sc.serverInfo()

#define a new scan
##newScan = '<commands><comment><address>0</address><text>Successfully adding a new scan</text></comment></commands>'

#clear scan server
print sc.clear()

#simulate the new scan
##print sc.simulate(newScan)

#submit the new scan and get the scan id
##sid = sc.submit(newScan,scanName='TestDemo')
##sid = str[4:sid.find('</id>')]

#get all scans
#print sc.scanInfo()

#abort the scan
#print sc.abort(sid)

