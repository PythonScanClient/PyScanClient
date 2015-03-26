'''
Created on 

@author: qiuyx
'''
from distutils.core import setup
setup(name='PyScanClient',
      version='0.9.5',
      description='Python Scna Server Client Lib',
      author='Qiu Yongxiang',
      author_email='qiuyongxiang05@gmail.com',
      url = 'https://github.com/ksdj/PyScanClient.git',
      packages= ['scan','scan.client','scan.commands','Test','example'],
      classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
     ],
      install_requires = []
    )
