from beamline_setup import *

# N-Dim scan with motors
# At each point, wait for pcharge which rises at about 1e9 per second
# Then log how many neutrons we got
cmds = ndim(('motor_x', 1, 3), ('motor_y', 1, 3),
            TakeData('pcharge', 3*1e9),
            'neutrons')

# Note how the defaults apply a readback to motors,
# how TakeData is expanded into basic commands etc.
print(cmds)

# The scan_client is already configured with the correct IP address
id = scan_client.submit(cmds)
print(scan_client.scanInfo(id))
print(scan_client.waitUntilDone(id))

