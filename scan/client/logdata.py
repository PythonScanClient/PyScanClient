"""Log Data Support
"""

import xml.etree.ElementTree as ET

from datetime import  datetime

def parseXMLData(xml_text):
    """Parse XML log data
    
    :param xml_text: XML Log data as returned from scan server
    
    :return: { 'device1': { 'id': ids.., 'time': times.., 'value': values.. } }
    """
    data = dict()
    xml = ET.fromstring(xml_text)
    if not xml.tag == "data":
        raise Exception("Expected <data>, but got <%s>" % xml.tag)
    
    for dev in xml.findall("device"):
        name = dev.find("name").text
        samples = dev.find("samples")
        ids = list()
        times = list()
        values = list()
        for sample in samples.findall("sample"):
            id = int(sample.attrib['id'])
            time = int(sample.find("time").text)
            try:
                value = float(sample.find("value").text)
            except:
                value = sample.find("value").text
            ids.append(id)
            times.append(time)
            values.append(value)
        
        data[name] = { 'id': ids, 'time': times, 'value': values }
    return data

class SampleIterator(object):
    """Sample iterator
    
    Iterator over samples of one device.
    At each step of the iteration, it provides a logged sample
    as a tuple containing
     1) Sample id
     2) Time stamp in Posix millisecond
     3) Value
     
    
    :param data: Data as returned by :func:`scan.client.scanclient.ScanClient.getData`
    :param device: Device for which to iterate over samples
    """
    def __init__(self, data, device):
        self.__ids = data[device]['id']
        self.__times = data[device]['time']
        self.__values = data[device]['value']
        self.__index = 0
        self.__size = len(self.__values)
        
    def __iter__(self):
        return self

    def next(self):
        """:return: Tuple with next ( id, time, value )"""
        if self.__index >= self.__size:
            raise StopIteration
        i = self.__index
        result = ( self.__ids[i], self.__times[i], self.__values[i] )
        self.__index += 1
        return result


def getDatetime(time):
    """Convert log time
    
    :param time: Posix millisecond timestamp of logged sample
    :return: datetime
    """ 
    secs = time / 1000
    return datetime.fromtimestamp(secs)


def createTable(data, *devices):
    """Create data table
    
    Aligns samples for given list of devices by sample ID.
    
    :param data: Data as returned by :func:`scan.client.scanclient.ScanClient.getData`
    :param devices: One or more devices
    
    :return: Table. result[0] has values for first device, result[1] for second device and so on.     
    """
    N = len(devices)
    iters = [ SampleIterator(data, device) for device in devices ]
    
    # 'Current' value for each iter or None when at end
    raw_data = list()
    for i in range(N):
        try:
            raw_data.append(iters[i].next())
        except StopIteration:
            raw_data.append(None)

    # Values for current 'row'
    values = [ None for i in range(N) ]
    result = [ list() for i in range(N) ]
    while True:
        # Locate smallest sample ID
        current_id = None
        for i in range(N):
            if raw_data[i]:
                if current_id is None   or  raw_data[i][0] < current_id:
                    current_id = raw_data[i][0]
        
        # Any data left?
        if current_id is None:
            break
        
        # For each device, get sample for current_id
        for i in range(N):
            if raw_data[i] is not None  and  raw_data[i][0] <= current_id:
                # Device has new raw data for current_id. Use it ..
                values[i] = raw_data[i][2]
                # .. and prepare for next iteration
                try:
                    raw_data[i] = iters[i].next()
                except StopIteration:
                    raw_data[i] = None
            # else: leave values[i] unchanged, repeating previous data
        
        # Add values for current_id to result
        for i in range(N):
            result[i].append(values[i])
    return result

