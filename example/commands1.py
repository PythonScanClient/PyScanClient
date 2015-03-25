from scan.commands import *

cmds = [
    Set('shutter:open', 1, completion=True),
    Loop('motor1', 1, 10, 0.5,
    [
       Set('daq:run', 1, completion=True),
       Delay(10),
       Set('daq:run', 0, completion=True),
    ], completion=True, readback='motor1.RBV', tolerance=0.5)
]

# .. and then submit to scan server for execution