from scan import *

# Assemble list of commands
cmds = [
    Set('shutter', 1),
    Loop('motor_x', 1, 10, 0.5,
    [
       Comment('daq:start'),
       Delay(10),
       Comment('daq:stop'),
       Log('motor_x')
    ], readback='motor_x', tolerance=0.5)
]

print("Basic list of commands:")
print(cmds)
# Result:
# [Set('shutter', 1), Loop('motor_x', 1, 10, 0.5, [ Comment('daq:start'),...

# Alternatively, use `CommandSequence` which can start
# empty or use list of commands
seq = CommandSequence(cmds)
# Commands can be added to sequence
seq.append(Comment('Done'))

print("`CommandSequence` results in nicer printout:")
print(seq)
# Result:
# [
#     Set('shutter', 1)
#     Loop('motor_x', 1, 10, 0.5,
#     [
#         Comment('daq:start'),
#         Delay(10),
#         Comment('daq:stop'),
#         Log('motor_x')
#     ], readback='motor_x', tolerance=0.5)
#     Comment('Done')
# ]

# .. and then submit to scan server for execution
client = ScanClient()
id = client.submit(seq)