'''
Copyright (c) 2014 
All rights reserved. Use is subject to license terms and conditions.
Created on Dec 30, 2014
Updated on Mar 19,2015
@author: Yongxiang Qiu
'''

import requests
from scan.commands.CmdSequence import CmdSequence

class ScanClient(object):
    '''
    The scan provides interfaces to interact with java-ScanServer,
    which includes methods such as Start,Pause,GetScanInfo... to manipulate 
    the behaviors and retrieve data from scan.
    '''
    __baseURL = None
    __serverResource = "/server"
    __serverInfoResource = "/info"
    __simulateResource = "/simulate"
    __scansResource = "/scans"
    __scansCompletedResource = "/completed"
    __scanResource = "/scan"
    
    def __new__(cls, host = 'localhost',port=4810):
        '''   
        Singleton method to make sure there is only one instance alive.
        '''
        
        if not hasattr(cls, 'instance'):
            cls.instance = super(ScanClient,cls).__new__(cls)
        return cls.instance
    
    def __init__(self, host = 'localhost',port=4810):
        
        self.__baseURL = "http://"+host+':'+str(port)
        
        try:  
            requests.get(self.__baseURL+'/scans', verify=False).raise_for_status()
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL
        
    def submit(self,cmds=None,scanName='UnNamed'):
        '''
        :param cmds: Support the following 3 types:
                    1.The .scn XML text
                    2.A CommandSequnce instance
                    3.A Python List
        '''
        try:
            if isinstance(cmds,str):
                self.__submitScanXML(cmds,scanName)
            
            elif isinstance(cmds,CmdSequence):
                self.__submitScanSequence(cmds, scanName)
            
            elif isinstance(cmds,list):
                self.__submitScanList(cmds,scanName)
        except:
            raise Exception, '''Invalid Commands input, must be one of these 3 types:
                             1.The .scn XML text. 
                             2.A CommandSequnce instance
                             3.An Array of commands
                             '''
        
        
    def __submitScanXML(self,scanXML=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from raw XML-form.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{scanId}</id>
        
        :param scanXML: The XML content of your new scan
        :param scanName: The name you want to give the new scan
        
        Usage::

        >>> import scan
        >>> ssc=ScanClient('localhost',4810)
        >>> scanId = ssc.__submitScanSequence(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        '''

        try:
            url = self.__baseURL+self.__scanResource+'/'+scanName
            r = requests.post(url = url,data = scanXML,headers = {'content-type': 'text/xml'}) 
        except:
            raise Exception, 'Failed to submit scan.'
        
        self.__curScanXML = scanXML
        self.__curScanName = scanName
        if r.status_code == 200:
            return r.text
        else:
            return r.status_code
    
    def __submitScanList(self,cmdList=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from Command Sequence.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{scanId}</id>
        
        :param cmdList: The Command Sequence of a new scan
        :param scanName: The name needed to give the new scan
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> cmds1 = [
                       Comment(comment='haha'),
                       Comment('hehe'),
                       Command(automatic=True),
                       DelayCommand(seconds=2.0),
                       Include(scanFile='1.scn',macros='macro=value'),
                       Log('shutter','xpos','ypos'),
                       Loop(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
                                   body=[Comment(comment='haha'),
                                         Command(automatic=True)
                                         ]),
                       Script('submit.py',1,'abc',0.05),
                       Set(device='shutter',value=0.1,completion=True,wait=False,tolerance=0.1,timeOut=0.1),
                       Wait(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
                    ]
        >>> scanId = ssc.__submitScanSequence(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        '''
        
        return self.__submitScanXML(self.genSCN4List(cmdList),scanName)
     
    def __submitScanSequence(self,cmdSeq=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from Command Sequence.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{scanId}</id>
        
        :param cmdSeq: The Command Sequence of a new scan
        :param scanName: The name needed to give the new scan
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> cmds1 = CmdSeq(
                       Comment(comment='haha'),
                       Comment('hehe'),
                       Command(automatic=True),
                       DelayCommand(seconds=2.0),
                       Include(scanFile='1.scn',macros='macro=value'),
                       Log('shutter','xpos','ypos'),
                       Loop(device='xpos',start=0.0,end=10.0,step=1.0,completion=True,wait=True,
                                   body=[Comment(comment='haha'),
                                         Command(automatic=True)
                                         ]),
                       Script('submit.py',1,'abc',0.05),
                       Set(device='shutter',value=0.1,completion=True,wait=False,tolerance=0.1,timeOut=0.1),
                       Wait(device='shutter',desiredValue=10.0,comparison='=',tolerance=0.1,timeout=5.0)
                    )
        >>> scanId = ssc.__submitScanSequence(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        '''
        
        if cmdSeq!=None:
            return self.__submitScanXML(cmdSeq.genSCN(),scanName)
        else:
            print 'No scan defined!'
            
    def genSCN4List(self,cmdList=None):
        result='<commands>'
        for c in cmdList:
            result+=c.genXML()
        
        result+='</commands>'
        return result
    
    def simulate(self,scanXML=None):
        '''
        Simulate a scan.
        
        Using   POST {BaseURL}/simulate
        Return  Success Messages in XML form
        
        :param scanXML: The XML content of your new scan
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> sid = ssc.simulate(scanXML='<commands><comment><address>0</address><text>Successfully simulating a new scan!</text></comment></commands>')
      
        '''
        
        r = requests.post(url = self.__baseURL+self.__simulateResource,data = scanXML,headers = {'content-type': 'text/xml'}) 
        if r.status_code == 200:
            return r.text
        else:
            return None
        
    def delete(self,scanID = None):
        '''
        Remove a unique scans.
        
        Using DELETE {BaseURL}/scan/{scanID}.
        Return HTTP status code.
        
        :param scanID: The id of scan you want to delete.Must be an integer.
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.delete(153)
      
        Return the status code. 0 if Error parameters.
        '''
        
        try:
            r=requests.delete(url = self.__baseURL+self.__scanResource+'/'+str(scanID))
            print 'scan %d deleted.'%scanID
        except:
            raise Exception, 'Failed to deleted scan '+str(scanID)
        return r.status_code

    def clear(self):
        '''
        Remove completed scan.
        
        Using DELETE {BaseURL}/scans/completed.
        Return HTTP status code.
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.clear()
        '''
        
        try:
            r = requests.delete(url = self.__baseURL+self.__scansResource+self.__scansCompletedResource)
            print 'All completed scans are deleted.'
        except:
            raise Exception, 'Failed to remove completed scan.'
        return r.status_code
    
    #############Detailed Design Needed#############
    def scanInfo(self,scanID = None,infoType = None):
        '''
        Get all information of one scan.
        Using  GET {BaseURL}/scan/{scanID}                - get scan info
               GET {BaseURL}/scan/{scanID}/commands       - get scan commands
               GET {BaseURL}/scan/{scanID}/data           - get scan data
               GET {BaseURL}/scan/{scanID}/last_serial    - get scan data's last serial
               GET {BaseURL}/scan/{scanId}/devices        - get devices used by a scan
        Return all info of one scan in XML form.
        
        :param scanID: The id of scan you want to get.Must be an integer.
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.scanInfo(153,scan)
        '''
                    
        try:
            if infoType == 'scan':
                url = self.__baseURL+self.__scanResource+'/'+str(scanID)
            else:
                url = self.__baseURL+self.__scanResource+'/'+str(scanID)+'/'+infoType
            r = requests.get(url)
        except:
            raise Exception, 'Failed to get info from scan '+str(scanID)
        return r.text
                
    def serverInfo(self):
        '''
        Get information of current server
        Using GET {BaseURL}/server/info
        Return:<Server></Server>
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.serverInfo()
        '''
        
        try:
            r = requests.get(url = self.__baseURL+self.__serverResource+self.__serverInfoResource)
        except:
            raise Exception, 'Failed to get info from scan server.'
        return r.text
        
    def scanList(self):
        '''
        Get information of all scans 
        Using GET {BaseURL}/scans - get all scan infos
        Return all info of all scans in XML form.
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.scanList()
        '''
        try:
            r = requests.get(url = self.__baseURL+self.__scansResource)
        except:
            raise Exception, 'Failed to get info from scan server.'
        return r.text

    def pause(self,scanID=None):
        ''' 
        Pause a running scan
        
        Using PUT {BaseURL}/scan/{id}/pause
        Return Http Status Code
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.pause(153)
        '''
        
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/pause')
        except:
            raise Exception, 'Failed to get info from scan server.'
        return r.status_code
        
    def abort(self,scanID=None):
        '''
        Abort running or paused scan
        
        Using PUT {BaseURL}/scan/{id}/abort
        Return Http Status Code
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.abort(153)
        '''

        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/abort')
        except:
            raise Exception, 'Failed to abort scan '+str(scanID)
        return r.status_code
    
    def resume(self,scanID=None):
        '''
        Resume paused scan
        Using PUT {BaseURL}/scan/{scanID}/resume
        
        Return Http Status Code
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.abort(153)
        '''
        
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/resume')
        except:
            raise Exception, 'Failed to resume scan ',scanID
        return r.status_code        
        
    def update(self,scanID=None,scanXML=None):
        '''
        Update property of a scan command.
        
        Using PUT {BaseURL}/scan/{scanID}/patch
        Return Http Status Code.
        
        Requires description of what to update:
          
            <patch>
                <address>10</address>
                <property>name_of_property</property>
                <value>new_value</value>
            </patch>
          
        '''
        
        try:
            r = requests.put(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/patch',data=scanXML,headers= {'content-type': 'text/xml'})
        except:
            raise Exception, 'Failed to resume scan '+str(scanID)
        return r.status_code
    
