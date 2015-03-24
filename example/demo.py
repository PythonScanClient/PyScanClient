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

'''
#get:
url = 'http://localhost:4810/scan/TestUrllib'
response = urllib2.urlopen(url).read()
print response

#post:
scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>'
req = urllib2.Request(url='http://localhost:4810/scan/TestUrllib',headers = {'Content-Type' : 'text/xml'},data=scanXML)
response = urllib2.urlopen(req).read()
print response
'''
#<commands><comment><text>haha</text></comment><comment><text>hehe</text></comment><config_log><automatic>true</automatic></config_log><delay><seconds>2.0</seconds></delay><include><scan_file>1.scn</scan_file><macros>macro=value</macros></include><log><devices><device>shutter</device><device>xpos</device><device>ypos</device></devices></log><loop><device>xpos</device><start>0.0</start><end>10.0</end><step>1.0</step><completion>true</completion><wait>true</wait><readback>xpos</readback><tolerance>0.1</tolerance><timeout>0.2</timeout><body><config_log><automatic>true</automatic></config_log><comment><text>haha</text></comment></body></loop><script><path>submit.py</path><arguments><argument>abc</argument><argument>0.05</argument></arguments><error_handler>1</error_handler></script><set><device>shutter</device><value>0.1</value><completion>true</completion><wait>true</wait><readback>pcharge</readback><tolerance>0.1</tolerance><timeout>0.1</timeout></set><wait><device>shutter</device><value>10.0</value><comparison>EQUALS</comparison><tolerance>0.1</tolerance><timeout>5.0</timeout></wait></commands>
#<commands><comment><text>haha</text></comment><comment><text>hehe</text></comment><config_log><automatic>true</automatic></config_log><delay><seconds>2.0</seconds></delay><include><scan_file>1.scn</scan_file><macros>macro=value</macros></include><log><devices><device>shutter</device><device>xpos</device><device>ypos</device></devices></log><loop><device>xpos</device><start>0.0</start><end>10.0</end><step>1.0</step><completion>true</completion><wait>true</wait><readback>xpos</readback><tolerance>0.1</tolerance><timeout>0.2</timeout><body><config_log><automatic>true</automatic></config_log><comment><text>haha</text></comment></body></loop><script><path>submit.py</path><arguments><argument>abc</argument><argument>0.05</argument></arguments><error_handler>1</error_handler></script><set><device>shutter</device><value>0.1</value><completion>true</completion><wait>true</wait><readback>pcharge</readback><tolerance>0.1</tolerance><timeout>0.1</timeout></set><wait><device>shutter</device><value>10.0</value><comparison>EQUALS</comparison><tolerance>0.1</tolerance><timeout>5.0</timeout></wait></commands>
#get the client instance
sc = ScanClient('localhost','4810')

####################2015-3-8 New ScanClient####################
#generalize client instance:
sc = ScanClient(host='localhost',port=4810)

cc = Comment(text='haha')
#Create Command Sequence:
cmds = CmdSequence(cc)
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
   #Script('test.py',1,'abc',0.05),
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
       #Script('test.py',1,'abc',0.05),
       Set(device='shutter',value=0.1,completion=True,tolerance=0.1,timeout=0.1),
       Wait(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
      ]

#print cc
#print 'cmds2:------',cmds2
print cmds.genSCN() 
#print sc.genSCN4List(cmds2)

#submit XML:
sc.submit(cmds.genSCN(),'TestSubmitXML')
#submit CmdSequence:
#sc.simulate(cmds.genSCN())

#sc.submit(cmds1, 'test')

#sc.abort(404)
sc.clear()
#sc.delete(399)
#sc.submit(cmds,'TestSubmitcmds1')
#submit List

#sc.submit(cmds2,'TestSubmitcmds2')
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
print sc.resume(410)

#sc.delete(402)
#simulate the new scan
##print sc.simulate(newScan)

#submit the new scan and get the scan id
##sid = sc.submit(newScan,scanName='TestDemo')
##sid = str[4:sid.find('</id>')]

#get all scans
#print sc.scanInfo()

#abort the scan
#print sc.abort(sid)

