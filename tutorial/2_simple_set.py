'''
This is an example how to use PyScanClient library to connect a scan server, and ask scan server to set a value
to pv 'motor_x'.

This example needs an example EPICS database, simulation.db, which could be found at: 
https://github.com/ControlSystemStudio/cs-studio/blob/master/applications/plugins/org.csstudio.scan/examples/
And it assumes the server running on localhost at port 4810.

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
from scan import Comment, Set

if __name__ == '__main__':
  
    client = ScanClient('localhost')
    
    # Assemble commands for a scan
    # Much more on that later...
    cmds = [ Comment('Hello'), Set('motor_x', 10) ]
    
    # Optionally, request a simulation that shows
    # how 'Include' and 'Loop' commands get expanded.
    simulation = client.simulate(cmds)
    print simulation
    
    # Submit scan for execution
    scid = client.submit(cmds, 'My First Scan')
    
    # Fetch information about scan
    info = client.scanInfo(scid)
    print info
    
    # Could poll scanInfo until info.isDone().
    # Shortcut:
    info = client.waitUntilDone(scid)
    print info
    