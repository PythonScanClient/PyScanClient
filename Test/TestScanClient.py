'''
Created on 2015-1-2

@author: qiuyx
'''

import unittest
from Scan import ScanClient
class TestScanClient(unittest.TestCase):
    
    __scanID=None
    __sc=None

    @classmethod
    def setUpClass(cls):
        
        #host = raw_input('Please input the scanserver IP:')
        #port = input('Please input the scanserver port:')
        cls.__sc = ScanClient('localhost',4810)
        rtval = cls.__sc.submit(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        #print 'rtval=',rtval
        if '<id' in rtval:
            cls.__scanID = rtval[4:rtval.find('</id>')]
        if cls.__scanID.isalnum():
            cls.__scanID = int(cls.__scanID)
        #cls.assertIsNotNone(cls.__scanID)
        print 'New scan is setted up, cls.__scanID = ' , cls.__scanID
        #print self.assertIsInstance(self.__sc, ScanClient)  
        print '\n=============Setup Done.=============\n'
        
    '''
    def test_submitScan(self):
        
        rtval = self.__sc.submit(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>',scanName='1stScan')
        #print 'rtval=',rtval
        if '<id' in rtval:
            self.__scanID = rtval[4:rtval.find('</id>')]
        if self.__scanID.isalnum():
            self.__scanID = int(self.__scanID)
        self.assertIsNotNone(self.__scanID)
        print 'self.__scanID = ' , self.__scanID
        print '\n=============Submit Done.=============\n'
    '''
        
    def test_clear(self):
        
        rtval = self.__sc.clear()
        self.assertTrue(rtval==200)
        print '\n=============RemoveCompleletedScan Done.=============\n' 
         
    def test_simulate(self):
        
        rtval = self.__sc.simulate(scanXML='<commands><comment><address>0</address><text>Successfully adding a new scan!</text></comment></commands>')
        self.assertIn('<simulation', rtval)
        print '\n=============Simulate Done.=============\n'
        
    def test_delete(self):

        rtval = self.__sc.delete(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============delete Done.=============\n'
 
    def test_scanList(self):

        rtval = self.__sc.scanList()
        self.assertIn('<scans',rtval)   
        print '\n=============scanInfo Done.=============\n'
        
    def test_getScanInfo(self):
        
        rtval = self.__sc.scanInfo(self.__scanID,'scan')
        self.assertIn('<scan',rtval)
        rtval = self.__sc.scanInfo(self.__scanID,'data')
        self.assertIn('<data',rtval)
        rtval = self.__sc.scanInfo(self.__scanID,'commands')
        self.assertIn('<commands',rtval)
        rtval = self.__sc.scanInfo(self.__scanID,'last_serial')
        self.assertIn('<serial',rtval)
        rtval = self.__sc.scanInfo(self.__scanID,'devices')
        self.assertIn('<devices',rtval)
        print '\n=============get Scaninfo Done.=============\n' 
        
    def test_pause(self):

        rtval = self.__sc.pause(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============Pause Done.=============\n' 
        
    def test_resume(self):

        rtval = self.__sc.resume(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============resume Done.=============\n' 

    def test_update(self):
        #rtval = self.__sc.update(170, )
        None
        
    def test_abort(self):

        rtval = self.__sc.abort(self.__scanID)
        self.assertTrue(rtval==200)
        print '\n=============abort Done.=============\n' 
    

#if __name__ == '__main__':
    #unittest.main()

print '\n',__name__
print  '==========================Test Start=========================='
suite = unittest.TestSuite()
suite.addTest(TestScanClient("test_simulate"))
#suite.addTest(TestScanClient("test_submitScan"))
suite.addTest(TestScanClient("test_scanList"))
suite.addTest(TestScanClient("test_clear"))
suite.addTest(TestScanClient("test_scanList"))
suite.addTest(TestScanClient("test_scanInfo"))
suite.addTest(TestScanClient("test_pause"))
suite.addTest(TestScanClient("test_resume"))
suite.addTest(TestScanClient("test_abort"))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)

#suite = unittest.TestLoader().loadTestsFromTestCase(TestScanClient)
