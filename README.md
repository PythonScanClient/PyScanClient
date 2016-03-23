PyScanClient
============
A collaboratively developed Python/Jython Scan Server Client.

Version Info
------------

See https://github.com/PythonScanClient/PyScanClient/blob/master/scan/version.py

Documentation
-------------

For snapshot, see http://ics-web.sns.ornl.gov/css/PyScanClient

Based on sphinx, http://sphinx-doc.org/

To install on Linux (RedHat):
    
    sudo yum install python-sphinx

To build:

    cd doc
    make clean html

Then view `doc/_build/html/index.html` in web browser.


This repository is at https://github.com/PythonScanClient/PyScanClient

When reaching initial production state, it may be transferred to https://github.com/ControlSystemStudio/PyScanClient

Install
-------

Global installation:

    sudo python setup.py install
   
Local installation:
   
    python setup.py install --prefix=$HOME
   
and then add the resulting $HOME/lib/python*/site-packages directory to your PYTHONPATH.


Uninstall
---------

    # cd to where it was installed
    rm -rf PyScanClient*.egg-info scan 
