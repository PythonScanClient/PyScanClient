.. _site:

Site Specific Setup
===================

For a site specific setup, refer to the following examples.

Configuration
-------------

Have all your scan scripts import a site specific top level python module
that does the following:

1) Import the scan modules that you intent to use
2) Import the SettingsBasedLoop, ..Set, ..Wait commands such
   that they replace the basic ones.
3) Install an instance of 
   :class:`~scan.util.scan_settings.ScanSettings`
   that is aware of your local devices.
4) Define meta-commands for accessing complex devices
   by combining basic commands into :class:`~scan.commands.sequence.Sequence` commands.
5) Provide a customized :class:`~scan.client.scanclient.ScanClient`
   that is aware of your scan server host.
6) Offers shortcuts to for example the table scan with pre/post commands required at your site.

.. literalinclude:: ../example/beamline_setup.py

Usage Examples
--------------

.. literalinclude:: ../example/beamline1.py

.. literalinclude:: ../example/beamline2.py

.. literalinclude:: ../example/beamline3.py



   