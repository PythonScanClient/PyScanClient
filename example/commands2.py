from scan import *
  
client = ScanClient('localhost')
print client

print client.serverInfo()

# Assemble commands for a scan
# Much more on that later...
cmds = CommandSequence(
    Log('loc://w(42)', 'loc://r(-1)'),
    Set('loc://w(42)', 1.0),
    Log('loc://w(42)', 'loc://r(-1)'),
    Set('loc://r(-1)', 1.0, readback='loc://w(42)', tolerance=0.1),
    Log('loc://w(42)', 'loc://r(-1)'),
    Set('loc://w(42)', 50.0, readback='loc://r(-1)', readback_value=1.0, tolerance=0.1),
    Log('loc://w(42)', 'loc://r(-1)')
)

print cmds

res = client.simulate(cmds)
print res['simulation']

# Submit scan for execution
id = client.submit(cmds, 'commands2.py')
print id


