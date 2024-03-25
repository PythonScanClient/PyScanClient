'''
This is an example how to use PyScanClient library to connect a scan server.
It assumes the server running on localhost at port 4810.

@author: shen, Kay Kasemir
'''
from scan import ScanClient

client = ScanClient('localhost')
print(client)

# show server information, which is in XML format.
print(client.serverInfo())
