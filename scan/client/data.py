'''
Created on Mar 27,2015

@author: qiuyX
'''
import xml.etree.ElementTree as ET

class Data(object):
    '''
    classdocs
    '''


    def __init__(self, Xml, last_serial):
        '''
        Constructor
        '''
        self.plainLog = self.__parsePlain(Xml)
        self.sparseLog = self.__parseMatrix(Xml,int(last_serial))
        
    def __parseMatrix(self,Xml,last_serial):
        '''
        Sparse Matrix Shape:
        for example : serail = 1~21
        sparseLog={
           'Xpos':{'serial':[0,  1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                   'time' : [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21],
                   'value': [0,  0, 1, 2, 3, 3, 3, 3, 3, 3,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X],
                   },
            'ypos':{'serial':[0,  1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                   'time' : [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21],
                   'value': [X,  X, X, X, 0, 1, 1, 2, 3, 4,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X,  X],
                    },
            ...
            
         'somePV':{'serial':[0,  1, 2, 3, 4, 5, 6, 7, 8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                   'time' : [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21]
                   'value': [v1,v2,v3,v4,v5,v6, X, X, X, ,X,  X,  X,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21]
                    }
        }
        
        Usage::
        #make an array (for numpy):
        ar = 
        [   #Values:
            [
            data['xpos']['value'],
            data['ypos']['value'],
            ...
            data['somePV']['value']
            ],
            
            #Times:
            [
            data['xpos']['time'],
            data['ypos']['time'],
            ...
            data['somePV']['time']
            ]
        ]
        ...
        #Data type Processing
        ...
        nar = numpy.array(ar)
        '''
        
        '''
        A plain data sets is a dictionary contains n key-pairs:
        {'pv1':dataDic1{},
         'pv2':dataDic2{},
          ...
         'pvn':dataDicn{}
        }
        for each key, its value is a dictionary contains 3 key-pairs:
         dataDic1{ 
         'serial' : [0,1,2,...,m],
         'time'   : [t1,t2,...,tm],
         'value'  : [v1,v2,...,vn]
         }
        So to make this data sets needs 2 level Loop:
        Loop1: for each PV
            Loop2 for each sample(0~m)
                make serial[]
                make time[]
                make value[]
            make serial,time,value into a dictionary 
        '''
        logdata = {}
        tree = ET.fromstring(Xml)
        channels = tree.findall('.//device')
        for channel in channels:
            #preparing:
            channel_data = {} #data of one channel  
    
            channel_name = channel.find('name').text #key
            samples = channel.findall('.//sample')
            timelist=[]
            vallist=[]
    
            #add 'serial' key and list:
            channel_data['serial'] = range(0,last_serial+1)
            j = 0
            for i in range(0,last_serial+1):
                if i == int(samples[j].attrib['id']):
                    timelist.append(samples[j].find('time').text)
                    vallist.append(samples[j].find('value').text)
                    j = j+1 if j<len(samples)-1 else len(samples)-1
                else:
                    timelist.append(None)
                    vallist.append(None)
    
            #add 'time' key and list:
            channel_data['time'] = timelist
            #add 'value' key and list:
            channel_data['value'] = vallist
            #add to datas{}:
            logdata[channel_name] = channel_data
            
        return logdata
    
    def __parsePlain(self,Xml):
        '''
        Plain Shape:
        for example : 
        plainLog={
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
        logdata = {}
        tree = ET.fromstring(Xml)
        channels = tree.findall('.//device')
        for channel in channels:
    
            channel_data = {} #data of one channel  
            channel_name = channel.find('name').text #key
            samples = channel.findall('.//sample')
    
            serialList=[]
            timeList=[]
            valList=[]
            for sample in samples:
                serialList.append(int(sample.attrib['id']))
                timeList.append(sample.find('time').text)
                valList.append(sample.find('value').text) 
    
            channel_data['serial'] = serialList
            channel_data['time'] = timeList
            channel_data['value'] = valList
            logdata[channel_name] = channel_data
        
        return logdata
        
    def PVlist(self):
        '''
        Get the list of all PV names.
        '''
        return list(self.plainLog)
        #return list(self.sparseLog)
        
    def PV(self,PVname):
        '''
        Get all data of a PV.
        
        @Param PVname: Name of the PV.
        
        Return: Dictionary of the data sets, like:
            {'serial':[...], 'time':[...], 'value'[...]}
        '''
        return self.plainLog[PVname]
        #return self.sparseLog[PVname]
    
    def PVvalue(self,PVname):
        '''
        Get all values of a PV, with
        
        @Param PVname: Name of the PV.
        
        Return: List of the values of the PV, like:
            [0.1,0.2,...,19.2]
        '''
        return self.plainLog[PVname]['value']
        #return self.sparseLog[PVname]['value']
    
    def PVtime(self,PVname):
        '''
        Get all timestamps of a PV.
        
        @Param PVname: Name of the PV.
        
        Return: List of the timestamps of the PV, like:
        ['1427396679782', '1427396679782', ... , '1427396679782']
        '''
        return self.plainLog[PVname]['time']
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
    def printPlain(self):
        '''
        Give a readable printing of the logged data.
        
        Usage::
        >>>sc = ScanClient('localhost',4810)
        >>>print sc.getData(449).printPlain()
        '''
        for key in self.plainLog:
            print key + ' : '
            print '{'
            print "    'serial' : "  + str(self.plainLog[key]['serial']) + ' ,'
            print "    'time'   : "  + str(self.plainLog[key]['time']) + ' ,'
            print "    'value'  : "  + str(self.plainLog[key]['value']) 
            print '} , \n'