.. _log_data:

Log Data
========

The scan server allows for basic logging via the :class:`~scan.commands.log.Log` command.
While not meant to provide complete data aquisition, it can be useful to track the
progress of a scan or to perform basic measurements that won't require a more sophisticated
data aquisition.

Each time a device is logged by the `Log` command, this stores

Sample ID:
    The first call to `Log` will use a sample ID of 0,
    the next call to `Log` will use a sample ID of 1 and so on.
    All samples logged with the same ID can thus be identified
    as having been logged by the same invocation of a `Log`
    command.

Time Stamp:
    The time stamp in Posix milliseconds as reported by the device.
    Note that this it not the time when the sample was logged, but the
    current time stamp of the data reported by the device.
    To identify which samples where logged at the same time,
    use the sample ID.

Value:
    The value is the current value of the device, either a number or a string.

.. literalinclude:: ../example/data1.py

Example
-------

API
---

.. autofunction:: scan.client.logdata.getDatetime

.. autofunction:: scan.client.logdata.iterateSamples

.. autofunction:: scan.client.logdata.iterateTable

.. autofunction:: scan.client.logdata.createTable

   