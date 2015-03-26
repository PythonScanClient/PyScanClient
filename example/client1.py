from scan.client.scanclient import ScanClient

from scan.commands import *
  
client = ScanClient('localhost')
print client
 
cmds = [ Comment('Hello'), Set('x', 10) ]
id = client.submit(cmds, 'My First Scan')
print id