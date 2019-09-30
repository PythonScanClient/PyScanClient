'''
Created on 

@author: qiuyx
'''
from distutils.core import setup
setup(name='PyScanClient',
      version='1.7.0',
      description='Python Scan Server Client Lib',
      author='Qiu Yongxiang, Kay Kasemir',
      author_email='qiuyongxiang05@gmail.com, kasemirk@ornl.gov',
      url = 'https://github.com/PythonScanClient',
      license = "Eclipse Public License - v 1.0",
      packages= [ 'scan', 'scan.client', 'scan.commands', 'scan.table', 'scan.util' ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
     ]
    )
