from scan.client.prelimdata import SampleIterator, getDatetime, parseXMLData, createTable

# client = ScanClient()
# id = client.submit(Loop('motor_x', 1, 5, 1, Loop('motor_y', 2, 4, 1, Log('motor_x', 'motor_y'))))
# client.waitUntilDone(id)

xml_text = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<data>
  <device>
    <name>motor_x</name>
    <samples>
      <sample id="0">
        <time>1427913270351</time>
        <value>1.0</value>
      </sample>
      <sample id="3">
        <time>1427913270595</time>
        <value>2.0</value>
      </sample>
      <sample id="6">
        <time>1427913270795</time>
        <value>3.0</value>
      </sample>
      <sample id="9">
        <time>1427913271076</time>
        <value>4.0</value>
      </sample>
      <sample id="12">
        <time>1427913271393</time>
        <value>5.0</value>
      </sample>
    </samples>
  </device>
  <device>
    <name>motor_y</name>
    <samples>
      <sample id="0">
        <time>1427913270352</time>
        <value>2.0</value>
      </sample>
      <sample id="1">
        <time>1427913270470</time>
        <value>3.0</value>
      </sample>
      <sample id="2">
        <time>1427913270528</time>
        <value>4.0</value>
      </sample>
      <sample id="3">
        <time>1427913270596</time>
        <value>2.0</value>
      </sample>
      <sample id="4">
        <time>1427913270695</time>
        <value>3.0</value>
      </sample>
      <sample id="5">
        <time>1427913270778</time>
        <value>4.0</value>
      </sample>
      <sample id="6">
        <time>1427913270795</time>
        <value>2.0</value>
      </sample>
      <sample id="7">
        <time>1427913270892</time>
        <value>3.0</value>
      </sample>
      <sample id="8">
        <time>1427913271018</time>
        <value>4.0</value>
      </sample>
      <sample id="9">
        <time>1427913271076</time>
        <value>2.0</value>
      </sample>
      <sample id="10">
        <time>1427913271170</time>
        <value>3.0</value>
      </sample>
      <sample id="11">
        <time>1427913271249</time>
        <value>4.0</value>
      </sample>
      <sample id="12">
        <time>1427913271393</time>
        <value>2.0</value>
      </sample>
      <sample id="13">
        <time>1427913271459</time>
        <value>3.0</value>
      </sample>
      <sample id="14">
        <time>1427913271559</time>
        <value>4.0</value>
      </sample>
    </samples>
  </device>
</data>
"""

# client.getData(id) calls this to turn the XML data into a data dict:
data = parseXMLData(xml_text)
print data

# Direct access to data dict
print "Times: ", [ str(getDatetime(time)) for time in  data['motor_x']['time'] ]
print "Values: ", data['motor_x']['value']

# Demo of sample iterator
for s in SampleIterator(data, 'motor_x'):
    print "%s (%2d): %s" % (str(getDatetime(s[1])), s[0], str(s[2]))

# Create table, i.e. align samples for different devices by sample ID:    
table = createTable(data, 'motor_x', 'motor_y')
print table[0]
print table[1]

# With numpy/scipy:  plot(table[0], table[1]) etc.
