.. _log_data:

Log Data
========

The scan server allows for basic logging via the :class:`scan.commands.log.Log` command.
While not meant to provide complete data aquisition, it can be useful to track the
progress of a scan or to perform basic measurements that won't require a more sophisticated
data aquisition.


.. literalinclude:: ../example/data1.py


API
---

.. autoclass:: scan.client.logdata.SampleIterator

.. autofunction:: scan.client.logdata.getDatetime

.. autofunction:: scan.client.logdata.createTable

   