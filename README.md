PyScanClient
============
A Python/Jython library for accessing the CS-Studio Scan Server.
Supports both the original Eclipse-based Scan Server and the Phoebus-based version.

Documentation
-------------

For latest snapshot of documentation, see https://controlssoftware.sns.ornl.gov/css_pyscanclient/.

To build local copy of documentation from sources, you need to install sphinx, http://sphinx-doc.org/.
To install on Linux (RedHat):
    
    sudo yum install python-sphinx

To build documentation from sources:

    cd doc
    make clean html

Then view `doc/_build/html/index.html` in web browser.

Install
-------

Global installation:

    sudo python setup.py install
   
Local installation:
   
    python setup.py install --prefix=$HOME
   
and then add the resulting `$HOME/lib/python*/site-package`s directory to your PYTHONPATH.

Minimal local installation:

    python setup.py build

and then add the resulting `build/lib` folder to your PYTHONPATH.

Uninstall
---------

    # cd to where it was installed
    rm -rf PyScanClient*.egg-info scan 

Running Tests
-------------

See Test/test_standalone

Version Info
------------

See https://github.com/PythonScanClient/PyScanClient/blob/master/scan/version.py

This repository is at https://github.com/PythonScanClient/PyScanClient
