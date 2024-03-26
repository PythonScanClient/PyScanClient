Overview
========

This package allows python or jython code to access the scan server.
You can assemble new scans, submit them, monitor their progress.

For a general overview of the scan system see
"CSS Scan System", Proceedings of ICALEPCS2013, San Francisco, CA, USA
( https://accelconf.web.cern.ch/ICALEPCS2013/papers/frcoaab01.pdf
or http://epaper.kek.jp/ICALEPCS2013/papers/frcoaab01.pdf )


Use Case: CS-Studio Displays
----------------------------

For routine execution of the same scan where just a few parameters change,
you can create a CS-Studio display for those parameters.
On the display, local or real PVs then allow users to for example configure
the start, end, and step size of a motor move.
A "Submit" button then invokes a jython script which assembles
a scan that moves a motor based on the values in those parameter PVs.


Use Case: Table-Based Scans
---------------------------

Scans that need to set devices like motors, temperature controllers etc.
to a list of desired positions, then maybe start data acquisition at each
point, wait for some condition, then move to the next point can often
be expressed in a concise table notation.

See :mod:`scan.table.table_scan`


Use Case: Custom Python Scripts
-------------------------------

Finally, custom Python scripts can assemble a set of commands,
see :ref:`scan_client`
and :ref:`scan_commands`.
