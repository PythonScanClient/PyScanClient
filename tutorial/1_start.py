'''
This is an example how to use PyScanClient library to connect a scan server.
It assumes the server running on localhost at port 4810.

The scan server is a RESTful based web service, which was developed at SNS.
Its binary nightly build could be found at:
https://ics-web.sns.ornl.gov/css/nightly/
and source code is managed at github:
https://github.com/ControlSystemStudio/cs-studio/tree/master/applications/plugins/org.csstudio.scan

The PyScanClient source code is managed at github:
https://github.com/PythonScanClient/PyScanClient

Created on Apr 17, 2015

@author: shen
'''
from scan import ScanClient

if __name__ == '__main__':
  
    client = ScanClient('localhost')
    print client
    
    # show server information, which is in XML format.
    print client.serverInfo()
