from scan import *
  
client = ScanClient('localhost')

# Log data during scan
cmds = [ Loop('motor_x', 1, 10, 1,
              [ 
                  Set('neutrons', 0),
                  Loop('motor_y', 1, 3, 1,
                       [
                           Delay(1),
                           Log('motor_y')
                       ]),
                  Log('motor_x', 'neutrons')
              ])
       ]
id = client.submit(cmds, 'Data Demo')
print "Waiting for scan %d to finish..." % id
info = client.waitUntilDone(id)
print "Number of log calls: %d" % client.lastSerial(id)

# Direct access to data dict
data = client.getData(id)
print data
print "Values: ", data['motor_x']['value']
print "Times: ", data['motor_x']['time']

# Convert times from posix millisecs into local datatime
print "Times: ", [ str(getDatetime(time)) for time in  data['motor_x']['time'] ]

# Demo of sample iterator
for s in iterateSamples(data, 'motor_x'):
    print "%s (%2d): %s" % (str(getDatetime(s[1])), s[0], str(s[2]))
 
# Create table, i.e. align samples for different devices by sample ID:    
table = createTable(data, 'motor_x', 'neutrons')
print "Positions: ", table[0]
print "Counts   : ", table[1]
for (pos, count) in zip(*table):
    print "Counts at motor position %g: %g" % (pos, count)
    
# Could plot this with numpy/scipy:  plot(table[0], table[1]) etc.

