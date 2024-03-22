Getting Started
===============

In the following, we describe the setup and some basic scan server interactions.

Initial Setup
-------------

We assume that you already have a recent version of EPICS base installed
with access to commands like `softIoc`, `caget`, `caput`.

The scan server is a CS-Studio service.
Both the scan server and the CS-Studio GUI can be built
from https://github.com/ControlSystemStudio/phoebus.
Binaries are for example available from
https://controlssoftware.sns.ornl.gov/css_phoebus/nightly/

All CS-Studio tools are based on Java. The CS-Studio GUI binary
may bundle a java runtime. If it includes a `jdk` folder, use that.
Otherwise fetch a Java runtime from https://jdk.java.net
Either way, declare your JDK and add its `bin` folder to the PATH::

  export JAVA_HOME=/path/to/jdk
  export PATH=$JAVA_HOME/bin:$PATH

Check::

  java -version

Assuming a binary, start the scan server like this::

   unzip scan-server.zip
   cd scan-server-*
   ./scan-server.sh

On success, note the REST URL and list of console commands::

   INFO ../ Scan Server (PID 1766187)
   INFO ... Scan Server REST interface on http://localhost:4810/index.html
   Scan Server Commands:
   help            -  Show commands
   ...
   shutdown        -  Stop the scan server

You would stop the scan server by typing `shutdown`, then restart via `scan-server.sh`.


Beamline Simulation
-------------------

Subsequent sections use a simple beamline simulation.

While we will use the complete PyScanClient later,
fetch it now to obtain that simulation and run it like this::

   git clone https://github.com/PythonScanClient/PyScanClient.git
   cd PyScanClient/example
   softIoc -d ioc/simulation.db 

Assuming you fetched a binary for CS-Studio, start the associated GUI like this::

   unzip phoebus-linux.zip 
   cd phoebus-*/
   ./phoebus.sh -resource /path/to/PyScanClient/example/opi/1_BeamLine.opi

.. image:: simulation.png

Familiarize yourself with the simulation.

* The "Beam" is mostly on, but occasionally turns off.
* Click on the "Shutter" to open or close it.
  While beam is on and the shutter open, the "Neutrons" counter increments.
  The "Proton Charge" increments as well, but you may
  only see that when you show it in "Probe" or a "Data Browser".
* Move the "X" and "Y" motor position sliders.
  There's a motor position that maximizes the signal on the detector
  (vertical orange bar).
* Move the "Device" setpoint slider and notice how its
  value (horizontal orange bar) follows with a delay.

Direct REST Access
------------------

The scan server is fundamentally a web service.
You will typically NOT directly interact with the web service,
but point your web browser to http://localhost:4810 and try the following.

* You should see a "Scan Server REST Interface" web page.
  Seeing that page confirms that the scan server is running.
  In an operational setup you might try to point a web browser on
  some control system operator interface host to http://name_of_server:4810
  to check network connectivity to the scan server.
* Follow the "/server/info" link.
  The XML format of the information is obviously not perfect for
  interactive use. For example, you would have to convert a UNIX epoch
  start time of "1711118742626" into "2024-03-22 10:45:42 EDT" to verify
  the scan server start time,
  but if all else fails such direct REST access can help you debug
  your setup on a low level.
* Back from the start page http://localhost:4810, click the
  "/scan/{name-of-new-scan}" link for submitting a new scan.
  The "Example" scan that is pre-populated in the web interface
  will set the "xpos" motor to 1, then 2, and log each value.
* "Submit" the scan and note in the CS-Studio GUI how the X motor is moved.
  The web interface will indicate the "ID" of the submitted scan and then
  switch to a list of scans. You may find the submitted scan either already finished
  or with an active "Delay 10.0 sec" command.
  Note that the web page needs a manual refresh to update.
  After a few manual refreshes, the scan should be "Finished".
* On the list of scans, follow the "(cmds)" link to view the commands of the scan,
  which should match what was submitted. Follow the "(data)" link and note how
  it lists one sample with value 1.0 and another with value 2.0.

Scan Server Console
-------------------

* In the scan server console, note how it logs each executed command.
  Type "help", then "scans". Type "commands ID" with the ID of the last submitted scan
  to get a list of commands. Type "data ID" to show the logged data.
* Stop the scan server by typing "shutdown" in its console, then restart the scan server.
  Try "scans" again.
  Note that "commands ID" will report an error because the list of commands
  is only held in memory for the duration of a scan server run.
  On the other hand, "data ID" will still show the logged data, which is persisted over
  scan server restarts.
  Those logged values are meant to help debug a scan or track its progress.
  It is neither meant to replace an archive system or experiment data aquision.
* Back from the start page http://localhost:4810, click the
  "/scan/{name-of-new-scan}" link and submit anoter example scan.

CS-Studio GUI
-------------

* In CS-Studio, invoke the menu Applications, Scan, Scan Monitor.
  You should see the last submitted scan as "Finished-OK",
  the others as simply "Logged".

* Right-click on any scan and open the "Data Table".
* Right-click no the "Finished" scan and open the "Scan Editor".
* In the scan editor, right-click to "Submit scan".
  It submits the same commands once more. While the scan is executing,
  the scan editor highlights the active command in green.
  Both the scan monitor and editor offer a red button to abort the scan.

.. image:: scan_monitor_editor.png

* In the scan editor, create a list of "Delay 1 sec" commands by deleting everything else,
  dragging noe "Delay" command from th palette into the editor,
  then use copy/paste from the context menu or Control-drag-drop to
  create about 10 delays.
* Submit the scan and note how it highlights the active delay command.
  Use the "pause" button in either the scan monitor or editor to pause and then resume
  the commands.
* Quickly submit the scan multiple times from the scan editor.
  Use the "Re-submit Scan" entry from the scan monitor context menu.
  Note how one scan executes, and additional scans are queued up to
  be executed next. Idle scans can be moved up or down in the list of queued
  scans, or aborted.
* In the scan monitor, selet a few older scans, right-click on them and "Remove selected". 

In an operational setup, the scan monitor can be very useful to monitor
the progress of queued and active scans.

The scan editor could be used to manually assemble small scans,
or to debug scans that have been submitted by other means.

The scan server will hold the commands of past scans in memory
and persist the logged data on disk, but this
is all meant to debug scans, not to replace data aquisition.
Based on memory usage thresholds, the scan server will automatically change
in-memory scans to only logged scans.
While the scan monitor can list many scans, reading the list of scans from
the server and displaying it will use noticable CPU once there are 10000 and more
scans in the list.
Periodically, for example when a new series of experiments start,
it is thus suggested to manually remove information for older scans,
either by deleting selected scans or by invoking "Remove completed scans"
from the scan monitor context menu.

PyScanClient
------------


Production Setup
----------------

In the above example we executed the scan server within a terminal window.
A production setup would typically run it as a Linux service using `procServ`,
https://github.com/ralphlange/procServ

