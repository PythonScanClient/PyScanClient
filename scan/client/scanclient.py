'''
Copyright (c) 2014 
All rights reserved. Use is subject to license terms and conditions.
Created on Dec 30, 2014
Updated on Mar 19,2015
@author: Yongxiang Qiu
'''

import urllib2
from scan.commands.commandsequence import CommandSequence
import xml.etree.ElementTree as ET

class scanclient(object):
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
       
    def __init__(self, host = 'localhost',port=4810):
        '''
        @param host: The IP address of the server.
        @param port: The IP port of the server.
        
        Usage::
        >>>sc = ScanClient('192.168.1.125','4811')
        '''
        #May implement a one to one host+port with instance in the future.
        self.__baseURL = "http://"+host+':'+str(port)

        conn = urllib2.urlopen(self.__baseURL+'/scans')
        try:
            conn.read()
        except Exception as ex:
            raise ex
        finally:
            conn.close()
    
    def __do_request(self,url=None,method=None,data=None):
        #handle all types of HTTP request.
        try:
            res_text = ''
            status_code = 0
            response = None
            #Register a Request Object with url:
            req = urllib2.Request(url)
            #Add XML header:
            req.add_header('content-type' , 'text/xml')
            #Get OpenerDirector Object
            opener = urllib2.build_opener()
            
            if method=='GET':
                response = opener.open(req)
                
            elif method=='POST':
                response = opener.open(req, data)
                
            elif method=='DELETE':
                req.get_method = lambda : 'DELETE'
                response = opener.open(req)
                
            elif method=='PUT':
                req.get_method = lambda : 'PUT'
                response = opener.open(req)
            else:
                raise Exception,'Undefined HttpRequest Type.'
            
            res_text = response.read()
            status_code = response.getcode()
            
            return res_text if status_code == 200 else status_code
              
        except Exception as ex:
            raise ex
        finally:
            response.close()
        
            
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
            
            elif isinstance(cmds,CommandSequence):
                self.__submitScanSequence(cmds, scanName)
            
            elif isinstance(cmds,list):
                self.__submitScanList(cmds,scanName)
            
            else:
                raise Exception, '''Invalid Commands input, must be one of these 3 types:
                1.The .scn XML text. 
                2.A CommandSequnce instance
                3.An Array of commands
                '''
        except Exception as e:
            raise e
            
        
        
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
        >>> scanId = ssc.__submitScanXML(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        '''
        url = self.__baseURL+self.__scanResource+'/'+scanName
        try:
            r =self.__do_request(url=url,method='POST',data=scanXML)
            return r
        except Exception,ex:
            raise Exception,ex
        
    
    def __submitScanList(self,cmdList=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from Command Sequence.
        
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
        >>> scanId = ssc.__submitScanList(cmds1)
        '''
        
        return self.__submitScanXML(self.genSCN4List(cmdList),scanName)
     
    def __submitScanSequence(self,cmdSeq=None,scanName='UnNamed'):
        '''
        Create and submit a new scan from Command Sequence.
        
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
        
        return self.__submitScanXML(cmdSeq.genSCN(),scanName)
            
    def genSCN4List(self,cmdList=None):
        xml = ET.Element('commands')
        for c in cmdList:
            xml.append(c.genXML())
        return ET.tostring(xml)
    
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
        url = self.__baseURL+self.__simulateResource
        try:
            r =self.__do_request(url=url,method='POST',data=scanXML)
            return r
        except:
            raise Exception, 'Failed to simulate scan.'
        
    def delete(self,scanID = None):
        '''
        Remove a completed scans.
        
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
            r=self.__do_request(url=self.__baseURL+self.__scanResource+'/'+str(scanID), method='DELETE')
            return r
        except Exception as ex:
            raise  ex
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
            r = self.__do_request(url=self.__baseURL+self.__scansResource+self.__scansCompletedResource, method='DELETE')
            return r
        except Exception as ex:
            raise ex
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
                    
        if infoType == 'scan':
            url = self.__baseURL+self.__scanResource+'/'+str(scanID)
        else:
            url = self.__baseURL+self.__scanResource+'/'+str(scanID)+'/'+infoType
        try:
            r = self.__do_request(url=url,method="GET")
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
            r = self.__do_request(url=self.__baseURL+self.__serverResource+self.__serverInfoResource,method='GET')
        except Exception as e:
            raise e 
        return r
        
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
            r = self.__do_request(url = self.__baseURL+self.__scansResource,method='GET')
        except Exception as ex:
            raise ex
        return r

    def pause(self,scanID=None):
        ''' 
        Pause a running scan
        
        Using PUT {BaseURL}/scan/{id}/pause
        Return Http Status Code.
        
        Usage::

        >>> import scan
        >>> ssc=scan('localhost',4810)
        >>> st = ssc.pause(153)
        '''
        
        try:
            url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/pause'
            r = self.__do_request(url=url, method='PUT')
            return r
        except Exception as ex:
            raise ex 
        
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
            url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/abort'
            r = self.__do_request(url=url, method='PUT')
            return r
        except Exception as ex:
            raise ex 
    
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
            url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/resume'
            r = self.__do_request(url=url, method='PUT')
            return r
        except Exception as ex:
            raise ex 
        
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
            r = self.__do_request(url=self.__baseURL+self.__scanResource+'/'+str(scanID)+'/patch',data=scanXML,method="PUT")
        except:
            raise Exception, 'Failed to resume scan '+str(scanID)
        return r.status_code
