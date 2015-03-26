
import unittest
import xml.etree.ElementTree as ET
from scan.commands import *

# These tests compare the XML as strings, even though for example
# both "<comment><text>Hello</text></comment>"
# and "<comment>\n  <text>Hello</text>\n</comment>"
# would be acceptable XML representations.
# Changes to the XML could result in the need to update the tests.
class CommandTest(unittest.TestCase):
    def testXMLEscape(self):
        # Basic comment
        cmd = Comment("Hello")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<comment><text>Hello</text></comment>")

        # Check proper escape of "less than"
        cmd = Comment("Check for current < 10")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<comment><text>Check for current &lt; 10</text></comment>")

    def testDelayCommand(self):
        # Basic set
        cmd = Delay(47.11)
        print cmd
        self.assertEqual(str(cmd), "Delay(47.11)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<delay><seconds>47.11</seconds></delay>")

    def testConfig(self):
        # Basic set
        cmd = ConfigLog(True)
        print cmd
        self.assertEqual(str(cmd), "ConfigLog(True)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<config_log><automatic>true</automatic></config_log>")

    def testSetCommand(self):
        # Basic set
        cmd = Set("some_device", 3.14)
        print cmd
        self.assertEqual(str(cmd), "Set('some_device', 3.14)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>3.14</value></set>")

        # Handle numeric as well as string for value
        cmd = Set("some_device", "Text")
        print cmd
        self.assertEqual(str(cmd), "Set('some_device', 'Text')")
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>Text</value></set>")

        # With completion
        cmd = Set("some_device", 3.14, completion=True)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>3.14</value><completion>true</completion></set>")

        # .. and timeout
        cmd = Set("some_device", 3.14, completion=True, timeout=5.0)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>3.14</value><completion>true</completion><timeout>5.0</timeout></set>")

        # Setting a readback PV (the default one) enables wait-on-readback
        cmd = Set("some_device", 3.14, completion=True, readback=True, tolerance=1, timeout=10.0)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>3.14</value><completion>true</completion><wait>true</wait><readback>some_device</readback><tolerance>1</tolerance><timeout>10.0</timeout></set>")

        # Setting a readback PV (a specific one) enables wait-on-readback
        cmd = Set("some_device", 3.14, completion=True, readback="some_device.RBV", tolerance=1, timeout=10.0)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>3.14</value><completion>true</completion><wait>true</wait><readback>some_device.RBV</readback><tolerance>1</tolerance><timeout>10.0</timeout></set>")

    def testParallel(self):
        # Nothing
        cmd = Parallel()
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<parallel />")

        # A few
        cmd = Parallel(Comment("One"), Comment("Two"))
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<parallel><body><comment><text>One</text></comment><comment><text>Two</text></comment></body></parallel>")

        # .. as list
        cmds = Comment("One"), Comment("Two")
        cmd = Parallel(cmds)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<parallel><body><comment><text>One</text></comment><comment><text>Two</text></comment></body></parallel>")

        cmd = Parallel(body=cmds)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<parallel><body><comment><text>One</text></comment><comment><text>Two</text></comment></body></parallel>")

        # With other parameters
        cmd = Parallel(cmds, timeout=10)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<parallel><timeout>10</timeout><body><comment><text>One</text></comment><comment><text>Two</text></comment></body></parallel>")

        cmd = Parallel(cmds, errhandler="MyHandler")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<parallel><body><comment><text>One</text></comment><comment><text>Two</text></comment></body><error_handler>MyHandler</error_handler></parallel>")

    def testLog(self):
        # One device
        cmd = Log("pv1")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<log><devices><device>pv1</device></devices></log>")

        # Nothing
        cmd = Log()
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<log />")

        # Several
        cmd = Log("pv1", "pv2", "pv3")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<log><devices><device>pv1</device><device>pv2</device><device>pv3</device></devices></log>")

        # .. provided as list
        devices_to_log = [ "pv1", "pv2", "pv3" ]
        cmd = Log(devices_to_log)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<log><devices><device>pv1</device><device>pv2</device><device>pv3</device></devices></log>")

    def testInclude(self):
        cmd = Include("start.scn")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<include><scan_file>start.scn</scan_file></include>")

        cmd = Include("start.scn", "macro=value")
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<include><scan_file>start.scn</scan_file><macros>macro=value</macros></include>")
        
    def testScript(self):
        cmd = Script("MyCustomScript")
        print cmd
        self.assertEqual(str(cmd), "Script('MyCustomScript')")
        self.assertEqual(ET.tostring(cmd.genXML()), "<script><path>MyCustomScript</path></script>")

        cmd = Script("MyCustomCommand", "arg1", 42.3)
        print cmd
        self.assertEqual(str(cmd), "Script('MyCustomCommand', 'arg1', 42.3)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<script><path>MyCustomCommand</path><arguments><argument>arg1</argument><argument>42.3</argument></arguments></script>")

    def testWait(self):
        cmd = Wait('device', 3.14)
        print cmd
        self.assertEqual(str(cmd), "Wait('device', 3.14)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<wait><device>device</device><value>3.14</value><comparison>EQUALS</comparison></wait>")

        cmd = Wait('counts', 1000, comparison='increase by', timeout=5.0, errhandler='someHandler')
        print cmd
        self.assertEqual(str(cmd), "Wait('counts', 1000, comparison='increase by', timeout=5, errhandler='someHandler')")
        self.assertEqual(ET.tostring(cmd.genXML()), "<wait><device>counts</device><value>1000</value><comparison>INCREASE_BY</comparison><timeout>5.0</timeout><error_handler>someHandler</error_handler></wait>")

    def testLoop(self):
        cmd = Loop('pv1', 1, 10, 0.1)
        print cmd
        self.assertEqual(str(cmd), "Loop('pv1', 1, 10, 0.1)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<loop><device>pv1</device><start>1</start><end>10</end><step>0.1</step><body /></loop>")

        cmd = Loop('pv1', 1, 10, 0.1, Delay(5))
        print cmd
        self.assertEqual(str(cmd), "Loop('pv1', 1, 10, 0.1, [ Delay(5) ])")
        cmd = Loop('pv1', 1, 10, 0.1, Delay(1), Delay(2))
        print cmd
        self.assertEqual(str(cmd), "Loop('pv1', 1, 10, 0.1, [ Delay(1), Delay(2) ])")
        cmd = Loop('pv1', 1, 10, 0.1, body= [ Delay(1), Delay(2) ])
        print cmd
        self.assertEqual(str(cmd), "Loop('pv1', 1, 10, 0.1, [ Delay(1), Delay(2) ])")
        self.assertEqual(ET.tostring(cmd.genXML()), "<loop><device>pv1</device><start>1</start><end>10</end><step>0.1</step><body><delay><seconds>1</seconds></delay><delay><seconds>2</seconds></delay></body></loop>")

        cmd = Loop('pv1', 1, 10, 0.1, Delay(1), Delay(2), readback=True)
        print cmd
        self.assertEqual(ET.tostring(cmd.genXML()), "<loop><device>pv1</device><start>1</start><end>10</end><step>0.1</step><wait>true</wait><readback>pv1</readback><tolerance>0.01</tolerance><body><delay><seconds>1</seconds></delay><delay><seconds>2</seconds></delay></body></loop>")

        cmd = Loop('pv1', 1, 10, 0.1, completion=True, timeout=10)
        print cmd
        self.assertEqual(str(cmd), "Loop('pv1', 1, 10, 0.1, completion=True, timeout=10)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<loop><device>pv1</device><start>1</start><end>10</end><step>0.1</step><completion>true</completion><timeout>10</timeout><body /></loop>")


    def testXMLSequence(self):
        cmds = CommandSequence()
        print cmds
        print cmds.toSeqString()
        self.assertEqual(len(cmds), 0)
        print cmds.genSCN()
        
        cmds = CommandSequence(Comment('One'))
        print cmds
        print cmds.toSeqString()
        self.assertEqual(len(cmds), 1)
        print cmds.genSCN()
       
        cmds = CommandSequence(Comment('One'), Comment('Two'))
        print cmds
        print cmds.toSeqString()
        self.assertEqual(len(cmds), 2)
        print cmds.genSCN()
        self.assertEqual("""<commands><comment><text>One</text></comment><comment><text>Two</text></comment></commands>""",
                         cmds.genSCN().replace("\n", "").replace(" ", ""))


        cmds = CommandSequence(Comment('One'))
        cmds.append(Comment('Two'))
        print cmds
        print cmds.toSeqString()
        self.assertEqual(len(cmds), 2)
        print cmds.genSCN()


        cmds = CommandSequence( ( Comment('One'), Comment('Two') ) )
        print cmds
        print cmds.toSeqString()
        self.assertEqual(len(cmds), 2)
        print cmds.genSCN()
        
        cmds = CommandSequence(Comment('Example'), Loop('pos', 1, 5, 0.5, Set('run', 1), Delay(2), Set('run', 0)))
        print cmds.toSeqString()
        

if __name__ == "__main__":
    unittest.main()