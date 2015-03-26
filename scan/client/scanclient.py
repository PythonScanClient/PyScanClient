'''
Copyright (c) 2014 
All rights reserved. Use is subject to license terms and conditions.
Created on Dec 30, 2014
Updated on Mar 19,2015
@author: Yongxiang Qiu, Kay Kasemir
'''

import time
import xml.etree.ElementTree as ET
import urllib
import urllib2

from scan.commands.commandsequence import CommandSequence
from scaninfo import ScanInfo

class ScanClient(object):
    """Client interface to the scan server
    
    :param host: The IP address or name of scan server host.
    :param port: The TCP port of the scan server.
    
    Example:
    
    >>> client = ScanClient('localhost')
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
        
    def serverInfo(self):
        """Get scan server information
        
        Provides version number, configuration, ... of current server
        
        Using `GET {BaseURL}/server/info`
        
        :return: XML with server info
        
        Usage::

        >>> client = ScanClient()
        >>> print client.serverInfo()
        """
        return self.__do_request(self.__baseURL + self.__serverResource + self.__serverInfoResource, 'GET')
                
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

    def submit(self, cmds, name='UnNamed'):
        """Submit scan to scan server for execution
        
        :param cmds: List of commands,
                     :class:`scan.commands.commandsequence.CommandSequence`
                     or text with raw XML format.
        :param name: Name of scan
        
        :return: ID of submitted scan
        
        Examples::
        
        >>> cmds = [ Comment('Hello'), Set('x', 10) ]
        >>> id = client.submit( cmds, "My First Scan")
        
        >>> cmds = CommandSequent(Comment('Hello'))
        >>> cmds.append(Set('x', 10))
        >>> id = client.submit( cmds, "My Second Scan")
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
        Return  <id>{id}</id>
        
        :param scanXML: The XML content of your new scan
        :param scanName: The name you want to give the new scan
        
        :return: Raw XML for scan ID

        Usage::

        >>> import scan
        >>> ssc=ScanClient('localhost',4810)
        >>> id = ssc.__submitScanXML(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
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
        
    def scanInfo(self, id):
        """Get information about a scan
        
        Using `GET {BaseURL}/scan/{id}`
              
        :param id: The ID of scan for which to fetch information.
        :return: :class:`scan.client.scaninfo.ScanInfo`
        
        Example::
        
        >>> client = ScanClient()
        >>> print client.scanInfo(42)
        """
        url = self.__baseURL+self.__scanResource+'/'+str(id)
        
        xml = self.__do_request(url)
        return ScanInfo(xml)
    
    # TODO: GET {BaseURL}/scan/{id}/commands       - get scan commands
    # TODO: GET {BaseURL}/scan/{id}/data           - get scan data
    # TODO: GET {BaseURL}/scan/{id}/last_serial    - get scan data's last serial
    # TODO: GET {BaseURL}/scan/{id}/devices        - get devices used by a scan
    
    def waitUntilDone(self, id):
        """Wait until scan finishes
        
        :param id: ID of scan on which to wait
        
        :return: Scan info
        """
        info = self.scanInfo(id)
        while not info.isDone():
            time.sleep(1)
            info = self.scanInfo(id)
        return info

    def pause(self, id=-1):
        """Pause a running scan
        
        :param id: ID of scan or -1 to pause current scan 
        
        Using `PUT {BaseURL}/scan/{id}/pause`
        
        Example::

        >>> id = client.submit(commands)
        >>> client.pause(id)
        """
        url = self.__baseURL + self.__scanResource + '/' + str(id) + '/pause'
        self.__do_request(url, 'PUT')

    def resume(self, id=-1):
        """Resume a paused scan
        
        :param id: ID of scan or -1 to resume current scan
         
        Using `PUT {BaseURL}/scan/{id}/resume`
        
        Example::
        
        >>> id = client.submit(commands)
        >>> client.pause(id)
        >>> client.resume(id)
        """
        url=self.__baseURL + self.__scanResource + '/' + str(id) + '/resume'
        self.__do_request(url, 'PUT')
        
    def abort(self, id=-1):
        """Abort a running or paused scan
        
        :param id: ID of scan or -1 to abort current scan

        Using `PUT {BaseURL}/scan/{id}/abort`
        
        Example::

        >>> id = client.submit(commands)
        >>> client.abort(id)
        """
        url = self.__baseURL + self.__scanResource + '/' + str(id) + '/abort'
        self.__do_request(url, 'PUT')
        
    def delete(self, id):
        """Remove a completed scan.
        
        Using `DELETE {BaseURL}/scan/{id}`
        
        :param id: The id of scan you want to delete.
        
        Example::

        >>> id = client.submit(commands)
        >>> client.abort(id)
        >>> client.delete(id)
        """
        self.__do_request(self.__baseURL + self.__scanResource + '/' + str(id), 'DELETE')
        
    def clear(self):
        """Remove all completed scans.
        
        Using `DELETE {BaseURL}/scans/completed`
        
        Usage::
        
        >>> client.clear()
        """
        self.__do_request(self.__baseURL + self.__scansResource + self.__scansCompletedResource, 'DELETE')
        
            
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

        
    
    def update(self,id=None,scanXML=None):
        '''
        Update property of a scan command.
        
        Using PUT {BaseURL}/scan/{id}/patch
        Return Http Status Code.
        
        Requires description of what to update:
          
            <patch>
                <address>10</address>
                <property>name_of_property</property>
                <value>new_value</value>
            </patch>
          
        '''
        
        try:
            r = self.__do_request(url=self.__baseURL+self.__scanResource+'/'+str(id)+'/patch',data=scanXML,method="PUT")
        except:
            raise Exception, 'Failed to resume scan '+str(id)
        return r.status_code
