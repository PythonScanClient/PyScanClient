from beamline_setup import *

scan.ls()

print scan.ndim(('xpos', 1, 10))
print scan.ndim(('xpos', 1, 10), Comment('New X'), ('ypos', 1, 3), TakeData('beam_monitor', 1e12), 'neutrons')

print scan.table( [ 'xpos', 'ypos',     'Wait For', 'Value'],
                [
                  [    1,   [ 2, 4, 6], 'counts'   ,  1000],
                  [    3,            8, 'counts'   ,  1000],
                ])