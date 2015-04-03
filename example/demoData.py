from scan.client.scanclient import ScanClient
from scan.client.data import Data, getDatetime, getTimeSeries, alignSerial, getTable
sc = ScanClient('localhost',4810)

#xml = sc.getData(449)
#ls = int(sc.lastSerial(449))
#print sc.getData(449).printPlain()

xml='''<data>
  <device>
    <name>pcharge</name>
    <samples>
      <sample id="10">
        <time>1427396679782</time>
        <value>0.0</value>
      </sample>
      <sample id="11">
        <time>1427396679782</time>
        <value>0.6</value>
      </sample>
      <sample id="12">
        <time>1427396679782</time>
        <value>0.7</value>
      </sample>
      <sample id="13">
        <time>1427396679782</time>
        <value>0.8</value>
      </sample>
      <sample id="14">
        <time>1427396679782</time>
        <value>1.1</value>
      </sample>
      <sample id="15">
        <time>1427396679782</time>
        <value>1.2</value>
      </sample>
      <sample id="16">
        <time>1427396679782</time>
        <value>1.5</value>
      </sample>
      <sample id="17">
        <time>1427396679782</time>
        <value>1.7</value>
      </sample>
      <sample id="18">
        <time>1427396679782</time>
        <value>1.9</value>
      </sample>
      <sample id="19">
        <time>1427396679782</time>
        <value>2.3</value>
      </sample>
      <sample id="20">
        <time>1427396679782</time>
        <value>2.6</value>
      </sample>
      <sample id="21">
        <time>1427396679782</time>
        <value>3.0</value>
      </sample>
    </samples>
  </device>
  <device>
    <name>xpos</name>
    <samples>
      <sample id="0">
        <time>1427396670265</time>
        <value>0.0</value>
      </sample>
      <sample id="1">
        <time>1427396670265</time>
        <value>0.0</value>
      </sample>
      
      <sample id="3">
        <time>1427396679900</time>
        <value>2.0</value>
      </sample>
      <sample id="4">
        <time>1427396679903</time>
        <value>3.0</value>
      </sample>
      <sample id="5">
        <time>1427396679903</time>
        <value>3.0</value>
      </sample>
      <sample id="6">
        <time>1427396679903</time>
        <value>3.0</value>
      </sample> 
      <sample id="7">
        <time>1427396679903</time>
        <value>3.0</value>
      </sample>
      <sample id="8">
        <time>1427396679903</time>
        <value>3.0</value>
      </sample>
      <sample id="9">
        <time>1427396679903</time>
        <value>3.0</value>
      </sample>
    </samples>
  </device>
  <device>
    <name>ypos</name>
    <samples>
      <sample id="2">
        <time>1427396679897</time>
        <value>1.0</value>
      </sample>
      <sample id="4">
        <time>1427396670265</time>
        <value>0.0</value>
      </sample>
      <sample id="5">
        <time>1427396679916</time>
        <value>1.0</value>
      </sample>
      <sample id="6">
        <time>1427396679916</time>
        <value>1.0</value>
      </sample>
      <sample id="7">
        <time>1427396679922</time>
        <value>2.0</value>
      </sample>
      <sample id="8">
        <time>1427396679927</time>
        <value>3.0</value>
      </sample>
      <sample id="9">
        <time>1427396679932</time>
        <value>4.0</value>
      </sample>
    </samples>
  </device>
</data>
'''
d = Data(Xml=xml)
getTimeSeries(d, 'xpos', 'datetime')[1][0] = 11
print getTimeSeries(d, 'xpos', 'datetime')
print '-----------------xpos----------------------'
it = alignSerial(d, 'xpos')
for t in it:
    print "%s : %s" %  (t[0], str(t[1]))
print '-----------------ypos----------------------'
it = alignSerial(d, 'ypos')
for t in it:
    print "%s : %s" %  (t[0], str(t[1]))
print '-----------------pcharge----------------------'
it = alignSerial(d, 'pcharge')
for t in it:
    print "%s : %s" %  (t[0], str(t[1]))

print '-----------------x, y----------------------'
print getTable(d, 'xpos', 'ypos', 'pcharge')

