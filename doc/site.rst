.. _site:

Site Specific Setup
===================

For a site specific setup, refer to the following examples.

Configuration
-------------

1) Create an instance of 
   :class:`~scan.util.scan_settings.ScanSettings`
   that is aware of your local devices.
2) Wrap some of the basic commands such that they use
   your settings.
3) Define meta-commands for accessing complex devices
   by combining basic commands into :class:`~scan.commands.sequence.Sequence` commands.
4) Provide a customized :class:`~scan.client.scanclient.ScanClient`
   that is aware of your scan server host and offers shortcuts
   to for example the table scan.

.. literalinclude:: ../example/beamline_setup.py

Usage Examples
--------------

.. literalinclude:: ../example/beamline1.py

.. literalinclude:: ../example/beamline2.py

.. literalinclude:: ../example/beamline3.py



   