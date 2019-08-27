'''
Copyright (c) 2014-2018
All rights reserved. Use is subject to license terms and conditions.
@author: Yongxiang Qiu, Kay Kasemir
'''

import time
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
try:
    from urllib import quote        # Python 2
except:
    from urllib.parse import quote  # Python 3
from scan.client.logdata import parseXMLData
from scan.commands.commandsequence import CommandSequence
from .scaninfo import ScanInfo

# Python code uses urllib2.
# When accessed from jython, there were two problems.
#
# 1) https://github.com/PythonScanClient/PyScanClient/issues/18
# urllib2 is based on _socket.py.
# Depending on how BOY invokes jython,
# even a new threadLocalStateInterpreter and a newly compiled
# script can end up with a cached binary for org.python.jython_2.7.0.release/Lib/_socket.py,
# where the _socket.NIO_GROUP has been shut down when the previous *.opi file closed
# its threadLocalStateInterpreter.
# Calls to urllib2 will then receive a connection error based on
# "RejectedExecutionException: event executor terminated".
# Workaround was to re-create the _socket.NIO_GROUP
# and call sys.registerCloser(_socket._shutdown_threadpool)
#
# 2) https://github.com/ControlSystemStudio/cs-studio/issues/2535
# After updating to jython 2.7.1, the HTTP 'POST' appeared limited
# to sending 65k of data.
#
# Workaround for both is to use Java HTTP API for jython
import os
if os.name == 'java':
    import java.lang
    from java.io import BufferedReader, InputStreamReader, OutputStream
    from java.net import HttpURLConnection, URL

    def perform_request(url, method='GET', data=None, timeout=None):
        try:
            connection = URL(url).openConnection()
            connection.setRequestProperty("Connection", "close")
            connection.setRequestProperty("User-Agent", "PyScanClient")
            connection.setRequestProperty("Accept", "text/xml")
            connection.setDoOutput(True)
            connection.setRequestMethod(method)
            if data is not None:
                data = java.lang.String(data).getBytes()
                connection.setRequestProperty("Content-Type", "text/xml")
                connection.setRequestProperty("Content-Length", str(len(data)))
                out = connection.getOutputStream()
                out.write(data)
                out.close()
    
            inp = BufferedReader(InputStreamReader(connection.getInputStream()))
            result = java.lang.StringBuilder()
            while True:
                line = inp.readLine()
                if line is None:
                    break
                result.append(line).append('\n')
            inp.close()
            result = result.toString()
            connection.disconnect()
            return result
        except java.lang.Exception as e:
            raise Exception("%s: %s" % (url, str(e)))

else:
    import requests

    def perform_request(url, method='GET', data=None, timeout=None):
        """Perform HTTP request with scan server
        
        :param url:    URL
        :param method: 'GET', 'PUT', ...
        :param data:   Optional data
       
        :return: XML response from scan server
        """
        response = None
        try:
            # PUT/POST header
            headers = { 'content-type': 'text/xml' }

            if method=='GET':
                if timeout:
                    response = requests.request('GET', url, timeout=timeout)
                else:
                    response = requests.request('GET', url)

            elif method=='POST':
                response = requests.request('POST', url, headers=headers, data=data)

            elif method=='DELETE':
                response = requests.request('DELETE', url)

            elif method=='PUT':
                response = requests.request('PUT', url, headers=headers, data=data)
            else:
                raise Exception('Undefined HttpRequest Type %s' % method)

        except requests.RequestException as e:
            raise Exception("Failed to reach scan server at %s: %s" % (url, e))

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception("Scan server at %s returned error code %d" % (url, e.response.code))

        return response.text


class ScanClient(object):
    """Client interface to the scan server
    
    :param host: The IP address or name of scan server host.
    :param port: The TCP port of the scan server.
    
    Example:
    
    >>> client = ScanClient('localhost')
    """
    __baseURL = None
       
    def __init__(self, host='localhost', port=4810):
        self.__host = host
        self.__port = int(port) #no matter what type of 'port' input, self._port keeps to be int.
        #May implement a one to one host+port with instance in the future.
        self.__baseURL = "http://" + self.__host + ':' + str(self.__port)

    
    def __repr__(self):
        return "ScanClient('%s', %d)" % (self.__host, self.__port)


    def serverInfo(self):
        """Get scan server information
        
        Provides version number, configuration, ... of current server
        
        Using `GET {BaseURL}/server/info`
        
        :return: XML with server info
        
        Usage::

        >>> client = ScanClient()
        >>> print client.serverInfo()
        """
        return perform_request(self.__baseURL + "/server/info")

                
    def simulate(self, cmds):
        """Submit scan to scan server for simulation
        
        :param cmds: List of commands,
                     :class:`~scan.commands.commandsequence.CommandSequence`
                     or text with raw XML format.
        
        :return: Simulation result as dictionary `{ 'simulation': "Printable text", 'seconds': 193.0 }`
        
        Example::

        >>> result = client.simulate([ Set('x', 5), Delay(2) ])
        >>> print result['simulation']
        """
        if isinstance(cmds, str):
            scan = cmds            
        elif isinstance(cmds, CommandSequence):
            scan = cmds.genSCN()
        else:
            # Warp list, tuple, other iterable
            scan = CommandSequence(cmds).genSCN()
            
        url = self.__baseURL + "/simulate"

        result = perform_request(url, 'POST', scan)
        xml = ET.fromstring(result)
        if xml.tag != 'simulation':
            raise Exception("Expected scan <simulation>, got <%s>" % xml.tag)
        simulation = xml.find('log').text
        seconds = float(xml.find('seconds').text)
        return { 'simulation': simulation, 'seconds': seconds }


    def submit(self, cmds, name='UnNamed', queue=True):
        """Submit scan to scan server for execution
        
        :param cmds: List of commands,
                     :class:`~scan.commands.commandsequence.CommandSequence`
                     or text with raw XML format.
        :param name: Name of scan
        :param queue: Submit to scan server queue, or execute as soon as possible?
        
        :return: ID of submitted scan
        
        Examples::
        
        >>> cmds = [ Comment('Hello'), Set('x', 10) ]
        >>> id = client.submit( cmds, "My First Scan")
        
        >>> cmds = CommandSequent(Comment('Hello'))
        >>> cmds.append(Set('x', 10))
        >>> id = client.submit( cmds, "My Second Scan")
        """
        quoted_name = quote(name, '')
        if isinstance(cmds, str):
            result = self.__submitScanXML(cmds, quoted_name, queue)     
        elif isinstance(cmds, CommandSequence):
            result = self.__submitScanSequence(cmds, quoted_name, queue)
        else:
            # Warp list, tuple, other iterable
            result = self.__submitScanSequence(CommandSequence(cmds), quoted_name, queue)
        
        xml = ET.fromstring(result)
        if xml.tag != 'id':
            raise Exception("Expected scan <id>, got <%s>" % xml.tag)
        return int(xml.text)


    def __submitScanXML(self, scanXML, scanName, queue=True):
        """Submit scan in raw XML-form.
        
        Using   POST {BaseURL}/scan/{scanName}
        Return  <id>{id}</id>
        
        :param scanXML: The XML content of your new scan
        :param scanName: The name you want to give the new scan
        :param queue: Submit to scan server queue, or execute as soon as possible?
        
        :return: Raw XML for scan ID

        Usage::

        >>> import scan
        >>> ssc=ScanClient('localhost',4810)
        >>> id = ssc.__submitScanXML(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        """
        url = self.__baseURL + "/scan/" + scanName
        if not queue:
            url = url + "?queue=false"
        r = perform_request(url, 'POST', scanXML)
        return r
    
            
    def __submitScanSequence(self, cmdSeq, scanName, queue=True):
        """Submit a CommandSequence
        
        :param cmdSeq: :class:`scan.commands.commandsequence.CommandSequence`
        :param scanName: The name needed to give the new scan
        :param queue: Submit to scan server queue, or execute as soon as possible?

        :return: Raw XML for scan ID
        """
        return self.__submitScanXML(cmdSeq.genSCN(),scanName, queue)
      
           
    def scanInfos(self, timeout=20):
        """Get information of all scans 
        
        Using `GET {BaseURL}/scans`
        
        :param timeout: Throws exception when no reply within that time in seconds
        :return: List of :class:`~scan.client.scaninfo.ScanInfo`
        
        Example::

        >>> infos = client.scanInfos()
        >>> print [ str(info) for info in infos ]
        """
        xml = perform_request(self.__baseURL + "/scans", timeout=timeout)
        scans = ET.fromstring(xml)
        result = list()
        for scan in scans.findall('scan'):
            result.append(ScanInfo(scan))
        return result


    def scanInfo(self, scanID, timeout=10):
        """Get information for a scan
        
        Using `GET {BaseURL}/scan/{id}`
              
        :param scanID: The ID of scan for which to fetch information.
        :param timeout: Throws exception when no reply within that time in seconds
        :return: :class:`~scan.client.scaninfo.ScanInfo`
        
        Example::
        
        >>> client = ScanClient()
        >>> print client.scanInfo(42)
        """
        xml = perform_request(self.__baseURL + "/scan/" + str(scanID), timeout=timeout)
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
        url = self.__baseURL + "/scan/" + str(scanID) + '/commands'
        xml = perform_request(url)
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
        url = self.__baseURL + "/scan/" + str(scanID) + '/last_serial'
        xml = perform_request(url)
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
        url = self.__baseURL + "/scan/" + str(scanID) + '/devices'
        xml = perform_request(url)
        return xml

    def __getInfo(self, scanID):
        """Keep getting scan info while disconnected/timed out"""
        while True:
            try:
                return self.scanInfo(scanID)
            except:
                time.sleep(1)

    def waitUntilDone(self, scanID):
        """Wait until scan finishes.
        
        On return, the scan has finished successfully.
        Can also be used for an older scan that has logged data,
        whereupon this call will return immediately.
        
        In case the scan failed or was aborted,
        an exception is raised.

        If scan information is not available
        (timeout while requesting it),
        keep checking.
        
        :param scanID: ID of scan on which to wait
        
        :return: Scan info
        :raise Exception: If scan was aborted or failed. 
        """
        while True:
            info = self.__getInfo(scanID)
            if info.state in ( 'Aborted', 'Failed' ):
                raise Exception(str(info))
            if info.isDone():
                return info
            time.sleep(1)


    def pause(self, scanID=-1):
        """Pause a running scan
        
        :param scanID: ID of scan or -1 to pause current scan 
        
        Using `PUT {BaseURL}/scan/{id}/pause`
        
        Example::

        >>> id = client.submit(commands)
        >>> client.pause(id)
        """
        url = self.__baseURL + "/scan/" + str(scanID) + '/pause'
        perform_request(url, 'PUT')


    def resume(self, scanID=-1):
        """Resume a paused scan
        
        :param scanID: ID of scan or -1 to resume current scan
         
        Using `PUT {BaseURL}/scan/{id}/resume`
        
        Example::
        
        >>> id = client.submit(commands)
        >>> client.pause(id)
        >>> client.resume(id)
        """
        url=self.__baseURL + "/scan/" + str(scanID) + '/resume'
        perform_request(url, 'PUT')


    def abort(self, scanID=-1):
        """Abort a running or paused scan
        
        :param scanID: ID of scan or -1 to abort current scan

        Using `PUT {BaseURL}/scan/{id}/abort`
        
        Example::

        >>> id = client.submit(commands)
        >>> client.abort(id)
        """
        url = self.__baseURL + "/scan/" + str(scanID) + '/abort'
        perform_request(url, 'PUT')


    def delete(self, scanID):
        """Remove a completed scan.
        
        Using `DELETE {BaseURL}/scan/{id}`
        
        :param scanID: The id of scan you want to delete.
        
        Example::

        >>> id = client.submit(commands)
        >>> client.abort(id)
        >>> client.delete(id)
        """
        perform_request(self.__baseURL + "/scan/" + str(scanID), 'DELETE')


    def clear(self):
        """Remove all completed scans.
        
        Using `DELETE {BaseURL}/scans/completed`
        
        Usage::
        
        >>> client.clear()
        """
        perform_request(self.__baseURL + "/scans/completed", 'DELETE')

    def patch(self, scanID, address, property, value):  # @ReservedAssignment
        """Update scan on server.
        
        This can be used to update parameters of an existing
        command in an existing scan on the server.
        
        In case the command had already been executed, the change
        has no effect.
        
        Using `PUT {BaseURL}/scan/{id}/patch`

        :param scanID: The id of scan you want to update.
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
        perform_request(self.__baseURL + "/scan/" + str(scanID) + '/patch', 'PUT', xml)


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
        url = self.__baseURL + "/scan/" + str(scanID) + '/data'
        xml = perform_request(url)
        return parseXMLData(xml)

