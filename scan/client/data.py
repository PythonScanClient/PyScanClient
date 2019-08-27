'''
Created on Mar 27,2015

@author: Yongxiang Qiu, Kay Kasemir
'''
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
from datetime import  datetime

def getTimeSeries(data, name, convert='plain'):
    '''Get values aligned by different types of time.

    :param name:  channel name
    :param convert:    plain -> timestamp as seconds since epoch
                    datetime -> datetime objects
    :return:  value list with time

    Example:
        
    >>> data.getTimeSeries(..)
    '''
        
    if convert == 'plain':
        return [ [t for t in data[name]['time'] ],  [v for v in data[name]['value']] ]
    elif convert == 'datetime':
        return [ [str(getDatetime(time)) for time in data[name]['time']], [ v for v in data[name]['value']] ]


def getDatetime(time):
    '''Convert log time
    
    :param time: Posix millisecond timestamp of logged sample
    :return: datetime
    '''
    secs = time / 1000.0
    return datetime.fromtimestamp(secs)


def alignSerial(data, channel):
    '''
    Iterate data by serial ID.
                          
    :param: channel: Name of channel(device) needed to be iterate.
    
    :return: ( (id1, value1, time1) ,(id2, value2, time2), ..., (idn, valuen, timen))
    '''
    R = list(range(len(data[channel]['id']))) 
    for i in iter(R):
        yield (data[channel]['id'][i], data[channel]['value'][i], data[channel]['time'][i])


##TODO: step
def alignTime(data, channel, intv = 0):
    
    '''
    Iterate data by time.
                          
    :param: channel: Name of channel(device) needed to be iterate.
    
    :return: Iterator object.   
    '''
    R = list(range(len(data[channel]['time'])))
    for i in iter(R):
        yield (data[channel]['time'][i], data[channel]['value'][i])


def getTable(data, *devices, **kwargs):
    '''Create data table
    
    Aligns samples for given list of devices by sample ID.
    Assuming that serialID in data is Ascending.
    Ignoring the serialID 'gap'.
                          
    :param devices: One or more devices
    :param kwargs:  with_id=True to add sample serial id,
                    with_time=True to add time (seconds since epoch)
    
    :return: Table. result[0],result[1], .. hold the sample ID (if with_id),
                                            the time (if with_time),
                                            then the values for first device, for second device and so on.
    '''
    with_id = kwargs['with_id'] if 'with_id' in kwargs else False
    with_time = kwargs['with_time'] if 'with_time' in kwargs else False
    
    devsIters = [ alignSerial(data, dev) for dev in devices]  # prepare devices iterators 
    cur_samps = [next(devIt) for devIt in devsIters]  # initial devices iterators  
    result = [[] for dev in devices]
    if with_id:
        result.insert(0, [])
    if with_time:
        result.insert(0, [])
    cur_id = -1  # current sample id
    cur_time = 0 # Current sample time
    index = 0
    
    while True:
        try :
            cur_id = min((samp[0] for samp in cur_samps if samp is not None))  # find smallest sample ID as current id
            cur_time = max((samp[2] for samp in cur_samps if samp is not None))  # find last time stamp
        except ValueError:  # finished
            break     

        data_col = 0
        if with_id:
            result[data_col].append(cur_id)
            data_col += 1      
        if with_time:
            result[data_col].append(cur_time)
            data_col += 1      
        for i in range(len(devsIters)):  # for each device ,there are 3 situations:
            if cur_samps[i] is None:  # 1. if device has been exhausted.
                result[data_col+i].append(result[data_col+i][index-1])  # continue with previous value
            
            elif cur_samps[i][0] == cur_id:  # 2. if serial_id is the current id ( means this device was logged at current serial_id)
                try:
                    result[data_col+i].append(cur_samps[i][1]) # fetch value
                    cur_samps[i] = next(devsIters[i]) # step iter of current device and its value
                except StopIteration:  # if current device is just exhausted
                    cur_samps[i] = None
                    
            elif cur_samps[i][0] > cur_id:  #3. if serial_id is in the future ( means this device was not logged at the current serial_id)
                if index == 0:  # 1st loop
                    result[data_col+i].append(None)
                else:
                    result[data_col+i].append(result[data_col+i][index-1])  # fetch and save the previous value
            
        index += 1            
    
    return result 


class Data(object):
    '''
    classdocs
    '''

    def __init__(self, Xml):
        '''
        Constructor
        '''
        self.__logData = self.__parseRaw(Xml)
        
    
    def __parseRaw(self,Xml):
        '''
        Raw Shape:
        for example : 
        logData={
           'Xpos':{'id':[0,  1, 2, 3, 4, 5, 6, 7, 8,  9],
                   'time' : [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10],
                   'value': [0,  0, 1, 2, 3, 3, 3, 3, 3,  3],
                   },
            'ypos':{'id':[4, 5, 6, 7, 8, 9],
                   'time' : [t1,t2,t3,t4,t5,t6],
                   'value':  [0, 1, 1, 2, 3, 4],
                    },
            ...
            
         'somePV':{'id':[0,  1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                   'time' : [t1,t2,t3,t4,t5,t6, t7, t8, t9,t10,t11,t12,t13,t14,t15,t16]
                   'value': [v1,v2,v3,v4,v5,v6, v7, v8, v9,v10,v11,v12,v13,v14,v15,v16]
                    }
        }
        
        '''
        channels = ET.fromstring(Xml).iter('device')
        
        logdata = {}
        for channel in channels:
            samples = channel.findall('.//sample')
            
            logdata[channel.find('name').text] = {
                            'id' : [int(sample.attrib['id']) for sample in samples],
                            'time' : [int(sample.find('time').text) for sample in samples],
                            'value' : [self.__types((sample.find('value').text)) for sample in samples]                
                            }

        return logdata


    def __types(self, text):
        '''
        Try to cast text to float or int.
        '''
        try:
            if '.' in text:
                return float(text)
            else:
                return int(text)
        except ValueError:
            return text
        finally:
            return text
        
        
    def __getitem__(self, key):
        return self.__logData[key]

  
    def PVlist(self):
        '''
        Get the list of all PV names.
        '''
        return list(self.__logData.keys())

   
    def PV(self, PVname):
        '''
        Get all data of a PV.
        
        :param PVname: Name of the PV.
        
        :return: Dictionary of the data sets, like:
            {'id':[...], 'time':[...], 'value'[...]}
        '''
        return self.__logData[PVname]


    def PVvalue(self, PVname):
        '''
        Get all values of a PV, with
        
        :param PVname: Name of the PV.
        
        :return: List of the values of the PV, like:
            [0.1,0.2,...,19.2]
        '''
        return self.__logData[PVname]['value']

   
    def PVtime(self, PVname):
        '''
        Get all timestamps of a PV.
        
        :param PVname: Name of the PV.
        
        :return: List of the timestamps of the PV, like:
        ['1427396679782', '1427396679782', ... , '1427396679782']
        '''
        return self.__logData[PVname]['time']


    def __str__(self):
        '''
        Give a readable printing of the logged data.
        '''
        prettyOut = ''
        for key in self.__logData:
            prettyOut += key + ' : \n'
            prettyOut += '{\n'
            prettyOut += "    'id' : "  + str(self.__logData[key]['id']) + ' ,\n'
            prettyOut += "    'time'   : "  + str(self.__logData[key]['time']) + ' ,\n'
            prettyOut += "    'value'  : "  + str(self.__logData[key]['value']) 
            prettyOut += '\n} , \n'
        return prettyOut

