'''
Created on Mar 27,2015

@author: qiuyX
'''
import xml.etree.ElementTree as ET
from datetime import  datetime
import copy

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
    secs = time / 1000
    return datetime.fromtimestamp(secs)


def alignSerial(data, channel):
    '''
    Iterate data by serial ID.
                          
    :param: channel: Name of channel(device) needed to be iterate.
    
    :return: ( (serial1, value1) ,(serial2, value2), ..., (serialn, valuen))
    '''
    R = range(len(data[channel]['serial'])) 
    for i in iter(R):
        yield (data[channel]['serial'][i], data[channel]['value'][i], data[channel]['time'][i])

##TODO: step
def alignTime(data, channel, step = 0):
    
    '''
    Iterate data by time.
                          
    :param: channel: Name of channel(device) needed to be iterate.
    
    :return: Iterator object.   
    '''
    R = range(len(data[channel]['time']))
    for i in iter(R):
        yield (data[channel]['time'][i], data[channel]['value'][i])

##TODO
def alignInterpo(data, channel):
    
    '''
    Iterate data by time.
                          
    :param: channel: Name of channel(device) needed to be iterate.
    
    :return: Iterator object.   
    '''

def getTable(data, *devices):
    '''Create data table
    
    Aligns samples for given list of devices by sample ID.
    Assuming that serialID in data is Ascending.
    Ignoring the serialID gap which all device come to.
    
    :param alignBy: serial -> align value by sample id.
                          time -> align value by timestamp
                          
    :param interpo:   step -> 
                    linear -> 
                          
    :param devices: One or more devices
    
    :return: Table. result[0] has values for first device, result[1] for second device and so on.
    '''
    
    devsIters = [ alignSerial(data, dev) for dev in devices]
    cur_samps = [devIt.next() for devIt in devsIters]
    result = [[] for dev in devices]
    cur_id = -1
    index = 0
    
    while True:
        
        try :
            cur_id = min((samp[0] for samp in cur_samps if samp is not None))  # find smallest sample ID
        except ValueError:  # finished
            break     
        
        for i in range(len(devsIters)):  # for each device
            if cur_samps[i] is None:  #if device has been exhausted.
                result[i].append(result[i][index-1])
            elif cur_samps[i][0] == cur_id:  # if serial_id is 'current'
                
                try:
                    result[i].append(cur_samps[i][1]) # fetch value
                    cur_samps[i] = devsIters[i].next() # step iter of current device  and its value
                except StopIteration:  #if current device exhausted
                    cur_samps[i] = None  
                    
            elif cur_samps[i][0] > cur_id:  # if serial_id is in the future
                if index == 0:  # 1st loop
                    result[i].append(None)
                else:
                    result[i].append(result[i][index-1])  # fetch and save the previous value
            
        index += 1            
    
    return result 
##TODO: Advanced getTable   
def getTableAdvanced(data, alignBy = 'serial', interpo = 'step', *devices):
    
    '''Create data table
    
    Aligns samples for given list of devices by sample ID.
    
    :param alignBy: serial -> align value by sample id.
                          time -> align value by timestamp
                          
    :param interpo:   step -> 
                    linear -> 
                          
    :param devices: One or more devices
    
    :return: Table. result[0] has values for first device, result[1] for second device and so on.     
    '''

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
           'Xpos':{'serial':[0,  1, 2, 3, 4, 5, 6, 7, 8,  9],
                   'time' : [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10],
                   'value': [0,  0, 1, 2, 3, 3, 3, 3, 3,  3],
                   },
            'ypos':{'serial':[4, 5, 6, 7, 8, 9],
                   'time' : [t1,t2,t3,t4,t5,t6],
                   'value':  [0, 1, 1, 2, 3, 4],
                    },
            ...
            
         'somePV':{'serial':[0,  1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                   'time' : [t1,t2,t3,t4,t5,t6, t7, t8, t9,t10,t11,t12,t13,t14,t15,t16]
                   'value': [v1,v2,v3,v4,v5,v6, v7, v8, v9,v10,v11,v12,v13,v14,v15,v16]
                    }
        }
        
        '''
        
        channels = ET.fromstring(Xml).iter('device')
        
        logdata = {}
        for channel in channels:
    
            samples = iter(channel.findall('.//sample'))
            serial_list, time_list, value_list=[],[],[]
            for sample in samples:
                serial_list .append( int(sample.attrib['id']) )
                time_list.append( int(sample.find('time').text) ) 
                value_list.append(self.__types((sample.find('value').text))) 
            logdata[channel.find('name').text] = {
                            'serial' : serial_list,
                            'time' : time_list,
                            'value' : value_list
                            }
            '''
            logdata[channel.find('name').text] = {
                            'serial' : [int(sample.attrib['id'] for sample in samples],
                            'time' : [int(sample.find('time').text) for sample in samples],
                            'value' : [self.__types((sample.find('value').text)) for sample in samples]
                            }
            '''
        return logdata

    def __types(self,s):
        
        if type(eval(s)) == type(1):
            return int(s)
        elif type(eval(s)) == type(1.0):
            return float(s)
        else:
            return s
    
    def __getitem__(self, key):
        return copy.deepcopy(self.__logData[key])
        
    
    def PVlist(self):
        '''
        Get the list of all PV names.
        '''
        return list(self.__logData)
        #return list(self.sparseLog)
        
    def PV(self, PVname):
        '''
        Get all data of a PV.
        
        @Param PVname: Name of the PV.
        
        Return: Dictionary of the data sets, like:
            {'serial':[...], 'time':[...], 'value'[...]}
        '''
        return self.__logData[PVname]
        #return self.sparseLog[PVname]

    def PVvalue(self, PVname):
        '''
        Get all values of a PV, with
        
        @Param PVname: Name of the PV.
        
        Return: List of the values of the PV, like:
            [0.1,0.2,...,19.2]
        '''
        return self.__logData[PVname]['value']
        #return self.sparseLog[PVname]['value']
    
    def PVtime(self, PVname):
        '''
        Get all timestamps of a PV.
        
        @Param PVname: Name of the PV.
        
        Return: List of the timestamps of the PV, like:
        ['1427396679782', '1427396679782', ... , '1427396679782']
        '''
        return self.__logData[PVname]['time']
        #return self.sparseLog[PVname]['time']   
 
    def printSparseMatrix(self):
        ##TODO
        '''
        Print a sparse matrix which is clear for viewing.
        for example, 
        serail: 0~21
        {
          #value:
          ['serial':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
           ########################################################################################
           'xpos'  :[0, 0, 1, 2, 3, 3, 3, 3, 3, 3,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X],
           'ypos'  :[X, X, X, X, 0, 1, 1, 2, 3, 4,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X],
        'pcharge'  :[X, X, X, X, X, X, X, X, X, X, 0.0,0.6,0.7,0.8,1,1,1.2,1.5,1.7,1.9,2.3,2.6,3.0]
          ],
          
          #time:
          ['serial':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
           ########################################################################################
           'xpos'  :[0, 0, 1, 2, 3, 3, 3, 3, 3, 3,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X],
           'ypos'  :[X, X, X, X, 0, 1, 1, 2, 3, 4,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X],
        'pcharge'  :[X, X, X, X, X, X, X, X, X, X, 0.0,0.6,0.7,0.8,1,1,1.2,1.5,1.7,1.9,2.3,2.6,3.0]
          ],
        }  
        '''


    def __str__(self):
        '''
        Give a readable printing of the logged data.
        
        Usage::
        >>>sc = ScanClient('localhost',4810)
        >>>print sc.getData(449).printRaw()
        '''
        prettyOut = ''
        for key in self.__logData:
            prettyOut += key + ' : \n'
            prettyOut += '{\n'
            prettyOut += "    'serial' : "  + str(self.__logData[key]['serial']) + ' ,\n'
            prettyOut += "    'time'   : "  + str(self.__logData[key]['time']) + ' ,\n'
            prettyOut += "    'value'  : "  + str(self.__logData[key]['value']) 
            prettyOut += '\n} , \n'
        return prettyOut
