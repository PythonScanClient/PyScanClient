Scan Client
===========

This example shows how to connect to the scan server,
submit a scan,
and monitor its progress using the basic API,
without using site-specific settings
or abstractions like the table-based scan.

Example
-------

.. literalinclude:: ../example/client1.py


API
---

.. autoclass:: scan.client.scanclient.ScanClient
   :members:

.. autoclass:: scan.client.scaninfo.ScanInfo
   :members:
   