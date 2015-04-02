from scan import *
  
client = ScanClient('localhost')

# Log data during scan
id = client.submit([ Loop('motor_x', 1, 10, 1,
                      [ Log('motor_x'),
                        Loop('motor_y', 1, 3, 1,
                              Log('motor_y'))
                      ])
                   ], 'Data Demo')
info = client.waitUntilDone(id)
print "Number of log calls: %d" % client.lastSerial(id)

# Direct access to data dict
data = client.getData(id)
print data

print "Values: ", data['motor_x']['value']
print "Times: ", data['motor_x']['time']
 
# Convert times in posix millisecs into local datatime
print "Times: ", [ str(getDatetime(time)) for time in  data['motor_x']['time'] ]
 
# Demo of sample iterator
for s in SampleIterator(data, 'motor_x'):
    print "%s (%2d): %s" % (str(getDatetime(s[1])), s[0], str(s[2]))
 
# Create table, i.e. align samples for different devices by sample ID:    
table = createTable(data, 'motor_x', 'motor_y')
print table[0]
print table[1]
# With numpy/scipy:  plot(table[0], table[1]) etc.

