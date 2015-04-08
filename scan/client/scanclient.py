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
from scan.client.logdata import parseXMLData
from scan.client.data import Data
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
        self.__port = int(port) #no matter what type of 'port' input, self._port keeps to be int.
        #May implement a one to one host+port with instance in the future.
        self.__baseURL = "http://"+self.__host+':'+str(self.__port)

    
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
                response = opener.open(req, data)
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
        return self.__do_request(self.__baseURL + self.__serverResource + self.__serverInfoResource)

                
    def simulate(self, cmds):
        """Submit scan to scan server for simulation
        
        :param cmds: List of commands,
                     :class:`~scan.commands.commandsequence.CommandSequence`
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
                     :class:`~scan.commands.commandsequence.CommandSequence`
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
      
           
    def scanInfos(self):
        """Get information of all scans 
        
        Using `GET {BaseURL}/scans`
        
        :return: List of :class:`~scan.client.scaninfo.ScanInfo`
        
        Example::

        >>> infos = client.scanInfos()
        >>> print [ str(info) for info in infos ]
        """
        xml = self.__do_request(self.__baseURL + self.__scansResource)
        scans = ET.fromstring(xml)
        result = list()
        for scan in scans.findall('scan'):
            result.append(ScanInfo(scan))
        return result


    def scanInfo(self, scanID):
        """Get information for a scan
        
        Using `GET {BaseURL}/scan/{id}`
              
        :param scanID: The ID of scan for which to fetch information.
        :return: :class:`~scan.client.scaninfo.ScanInfo`
        
        Example::
        
        >>> client = ScanClient()
        >>> print client.scanInfo(42)
        """
        xml = self.__do_request(self.__baseURL + self.__scanResource + '/' + str(scanID))
        return ScanInfo(ET.fromstring(xml))


    def scanCmds(self, scanID):
        """Get the commands of scan.
        
        Reads scan commands from scan server.
        Only possible for scans that are still available
        on the server, not for older scans that only
        have logged data but no command detail.
        
        :param scanID::  The ID of scan for which to fetch information.
        
        :return: Scan commands in XML format of a scan.
        
        Example::
        
        >>> client = ScanClient()
        >>> scanid = client.submit(...someCMDs...)
        >>> # Submit it again:
        >>> client.submit(client.scanCmds(scanid))
        """
        url = self.__baseURL + self.__scanResource + '/' + str(scanID)+'/commands'
        xml = self.__do_request(url)
        return xml


    def lastSerial(self, scanID):
        """Get the last log data serial.
        
        Obtains the serial ID of the last logged sample of a scan.
        Allows clients which monitor the progress of a scan to poll
        for changes in the logged data without always having to pull
        the complete data log.
        
        :param scanID: The ID of scan for which to fetch information.
        
        :return: Id of last logged sample of the scan.
        
        Example::
        
        >>> last_log_fetched = -1
        >>> while not client.scanInfo(id).isDone:
        >>>     last_logged = client.lastSerial(id)
        >>>     if last_log_fetched != last_logged:
        >>>        # .. fetch logged data, because it has changed..
        >>>        last_log_fetched = last_logged
        >>>     time.sleep(10
        """
        url = self.__baseURL + self.__scanResource + '/' + str(scanID)+'/last_serial'
        xml = self.__do_request(url)
        ET.fromstring(xml)
        return int(ET.fromstring(xml).text)


    def scanDevices(self, scanID=-1):
        """Get list of devices used by scan.
        
        :param scanID: The ID of scan that is still held in scan server,
                       -1 to fetch default devices.
        
        Provides a list of devices used by a scan.
        For a running scan, this includes devices accessed
        in the pre- and post-scan.
        Also includes devices configured with alias names,
        but not necessarily used by the scan.
        
        :return: XML with info about devices.
        """
        url = self.__baseURL + self.__scanResource + '/' + str(scanID)+'/devices'
        xml = self.__do_request(url)
        return xml


    def waitUntilDone(self, scanID):
        """Wait until scan finishes
        
        :param scanID: ID of scan on which to wait
        
        :return: Scan info
        """
        info = self.scanInfo(scanID)
        while not info.isDone():
            time.sleep(1)
            info = self.scanInfo(scanID)
        return info


    def pause(self, scanID=-1):
        """Pause a running scan
        
        :param scanID: ID of scan or -1 to pause current scan 
        
        Using `PUT {BaseURL}/scan/{id}/pause`
        
        Example::

        >>> id = client.submit(commands)
        >>> client.pause(id)
        """
        url = self.__baseURL + self.__scanResource + '/' + str(scanID) + '/pause'
        self.__do_request(url, 'PUT')


    def resume(self, scanID=-1):
        """Resume a paused scan
        
        :param scanID: ID of scan or -1 to resume current scan
         
        Using `PUT {BaseURL}/scan/{id}/resume`
        
        Example::
        
        >>> id = client.submit(commands)
        >>> client.pause(id)
        >>> client.resume(id)
        """
        url=self.__baseURL + self.__scanResource + '/' + str(scanID) + '/resume'
        self.__do_request(url, 'PUT')


    def abort(self, scanID=-1):
        """Abort a running or paused scan
        
        :param scanID: ID of scan or -1 to abort current scan

        Using `PUT {BaseURL}/scan/{id}/abort`
        
        Example::

        >>> id = client.submit(commands)
        >>> client.abort(id)
        """
        url = self.__baseURL + self.__scanResource + '/' + str(scanID) + '/abort'
        self.__do_request(url, 'PUT')


    def delete(self, scanID):
        """Remove a completed scan.
        
        Using `DELETE {BaseURL}/scan/{id}`
        
        :param scanID: The id of scan you want to delete.
        
        Example::

        >>> id = client.submit(commands)
        >>> client.abort(id)
        >>> client.delete(id)
        """
        self.__do_request(self.__baseURL + self.__scanResource + '/' + str(scanID), 'DELETE')


    def clear(self):
        """Remove all completed scans.
        
        Using `DELETE {BaseURL}/scans/completed`
        
        Usage::
        
        >>> client.clear()
        """
        self.__do_request(self.__baseURL + self.__scansResource + self.__scansCompletedResource, 'DELETE')

 
    def patch(self, id, address, property, value):
        """Update scan on server.
        
        This can be used to update parameters of an existing
        command in an existing scan on the server.
        
        In case the command had already been executed, the change
        has no effect.
        
        Using `PUT {BaseURL}/scan/{id}/patch`

        :param id: The id of scan you want to update.
        :param address: Address of the command to update.
                        Counted within the scan starting at 0.
        :param property: The property of the command to update.
        :param value: The new value for that property.
        
        Example::
        
        >>> id = client.submit([ Delay(5), Set('motor_x', 10) ], 'Changing...')
        >>> client.pause(id)
        >>> # Want to set 'motor_x' to 5 instead of 10
        >>> client.patch(id, 1, 'value', 5)
        >>> client.resume(id)
        """
        xml = "<patch><address>%d</address><property>%s</property><value>%s</value></patch>" % (address, property, str(value))
        self.__do_request(self.__baseURL + self.__scanResource + '/' + str(id) + '/patch', 'PUT', xml)


    def getData(self, scanID):
        """Fetch logged data of a scan
        
        :param scanID: ID of scan
        
        :return: Data dictionary
        
        Example:
           >>> data = client.getData(id)
           >>> print data
           
        Format of the data::
        
           { 'device1': {'id': [0, 1, 2, 3, 4 ],
                         'value': [2.0, 3.0, 4.0, 2.0, 4.0],
                         'time': [1427913270352, 1427913270470, 1427913270528, 1427913270596, 1427913270695]
                        },
             'device2': {'id': [0, 3, 6, 9, 12],
                         'value': [1.0, 2.0, 3.0, 4.0, 5.0],
                         'time': [1427913270351, 1427913270595, 1427913270795, 1427913271076, 1427913271393]
                        }
           }

        The data dictionary has one entry per logged device.
        Its value is again a dictionary with entries
        
        id:
           Sample IDs, starting from 0
        value:
           Sample values
        time:
           Times in Posix milliseconds
        """
        url = self.__baseURL + self.__scanResource + '/' + str(scanID)+'/data'
        xml = self.__do_request(url)
        return parseXMLData(xml)

