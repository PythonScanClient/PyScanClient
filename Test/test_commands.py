
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


    def testSetCommand(self):
        # Basic set
        cmd = Set("some_device", 3.14)
        print cmd
        self.assertEqual(str(cmd), "Set('some_device', value=3.14)")
        self.assertEqual(ET.tostring(cmd.genXML()), "<set><device>some_device</device><value>3.14</value></set>")

        # Handle numeric as well as string for value
        cmd = Set("some_device", "Text")
        print cmd
        self.assertEqual(str(cmd), "Set('some_device', value='Text')")
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

        cmd = Parallel(cmds, errHandler="MyHandler")
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

if __name__ == "__main__":
    unittest.main()