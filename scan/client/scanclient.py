'''
Copyright (c) 2014 
All rights reserved. Use is subject to license terms and conditions.
Created on Dec 30, 2014
Updated on Mar 19,2015
@author: Yongxiang Qiu
'''

import urllib
import urllib2
from scan.commands.commandsequence import CommandSequence
import xml.etree.ElementTree as ET

class ScanClient(object):
    """Client interface to the scan server
    
    :param host: The IP address or name of scan server host.
    :param port: The TCP port of the scan server.
    
    Example:
        >>>sc = ScanClient('localhost')
    """
    __baseURL = None
    __serverResource = "/server"
    __serverInfoResource = "/info"
    __simulateResource = "/simulate"
    __scansResource = "/scans"
    __scansCompletedResource = "/completed"
    __scanResource = "/scan"
       
    def __init__(self, host='localhost', port=4810):
        self.__host = host
        self.__port = port
        #May implement a one to one host+port with instance in the future.
        self.__baseURL = "http://"+host+':'+str(port)
    
    def __repr__(self):
        return "ScanClient('%s', %d)" % (self.__host, self.__port)
    
    def __do_request(self, url, method='GET', data=None):
        """Perform HTTP request with scan server
        
        :param url:    URL
        :param method: 'GET', 'PUT', ...
        :param data:   Optional data
       
        :return: XML response from scan server
        """
        response = None
        try:
            # Register a Request Object with url:
            req = urllib2.Request(url)
            # Add XML header
            if data is not None:
                req.add_header('content-type' , 'text/xml')
            # Get OpenerDirector Object
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
                raise Exception('Undefined HttpRequest Type %s' % method)
            
            return response.read()
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                raise Exception("Failed to reach scan server at %s:%d: %s" % (self.__host, self.__port, e.reason))
            elif hasattr(e, 'code'):
                raise Exception("Scan server at %s:%d returned error code %d" % (self.__host, self.__port, e.code))
        finally:
            if response:
                response.close()
        
            
    def submit(self, cmds, name='UnNamed'):
        """Submit scan to scan server for execution
        
        :param cmds: List of commands,
                     :class:`scan.commands.commandsequence.CommandSequence`
                     or text with raw XML format.
        :param name: Name of scan
        
        :return: ID of submitted scan
        """
        quoted_name = urllib.quote(name, '')
        if isinstance(cmds, str):
            result = self.__submitScanXML(cmds, quoted_name)            
        elif isinstance(cmds, CommandSequence):
            result = self.__submitScanSequence(cmds, quoted_name)
        else:
            # Warp list, tuple, other iterable
            result = self.__submitScanSequence(CommandSequence(cmds), quoted_name)
        
        xml = ET.fromstring(result)
        if xml.tag != 'id':
            raise Exception("Expected scan <id>, got <%s>" % xml.tag)
        return int(xml.text)
        
        
    def __submitScanXML(self, scanXML, scanName):
        """Submit scan in raw XML-form.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{scanId}</id>
        
        :param scanXML: The XML content of your new scan
        :param scanName: The name you want to give the new scan
        
        :return: Raw XML for scan ID

        Usage::

        >>> import scan
        >>> ssc=ScanClient('localhost',4810)
        >>> scanId = ssc.__submitScanXML(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        """
        url = self.__baseURL + self.__scanResource + '/' + scanName
        r = self.__do_request(url, 'POST', scanXML)
        return r
        
    def __submitScanSequence(self, cmdSeq, scanName):
        """Submit a CommandSequence
        
        :param cmdSeq: :class:`scan.commands.commandsequence.CommandSequence`
        :param scanName: The name needed to give the new scan

        :return: Raw XML for scan ID
        """
        return self.__submitScanXML(cmdSeq.genSCN(),scanName)
            
    
    def simulate(self, cmds):
        """Submit scan to scan server for simulation
        
        :param cmds: List of commands,
                     :class:`scan.commands.commandsequence.CommandSequence`
                     or text with raw XML format.
        
        :return: Simulation result
        """
        if isinstance(cmds, str):
            scan = cmds            
        elif isinstance(cmds, CommandSequence):
            scan = cmds.genSCN()
        else:
            # Warp list, tuple, other iterable
            scan = CommandSequence(cmds).genSCN()
            
        url = self.__baseURL + self.__simulateResource

        simulation = self.__do_request(url, 'POST', scan)
        return simulation
        
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
