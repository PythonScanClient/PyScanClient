from scan.client.scanclient import ScanClient
from scan.commands.delay import Delay
client = ScanClient()
cmds = [ Delay(1.0) ]
client.submit(cmds, "Test")
