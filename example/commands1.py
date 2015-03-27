from scan import *

# Assemble list of commands
cmds = [
    Set('shutter:open', 1, completion=True),
    Loop('motor1', 1, 10, 0.5,
    [
       Set('daq:run', 1, completion=True),
       Delay(10),
       Set('daq:run', 0, completion=True),
    ], completion=True, readback='motor1.RBV', tolerance=0.5)
]

print cmds
# Result:
# [Set('shutter:open', 1, completion=True), Loop('motor1', 1, 10, 0.5, ...

# Alternatively, use `CommandSequence` which can start
# empty or use list of commands
seq = CommandSequence(cmds)
# Commands can be added to sequence
seq.append(Comment('Done'))

# `CommandSequence` results in nicer printout
print seq
# Result:
# [
#     Set('shutter:open', 1, completion=True)
#     Loop('motor1', 1, 10, 0.5,
#     [
#         Set('daq:run', 1, completion=True),
#         Delay(10),
#         Set('daq:run', 0, completion=True),
#     ], completion=True, readback='motor1.RBV', tolerance=0.5)
#     Comment('Done')
# ]


# .. and then submit to scan server for execution
client = ScanClient()
id = client.submit(seq)