
print """
Version Info
============

To obtain version info::


   from scan.version import __version__, version_history
   print __version__
   print version_history
"""

import sys
sys.path.append("..")
from scan.version import __version__, version_history

print "Version history::"

for line in version_history.splitlines():
    print ("   " + line)
