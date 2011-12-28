#!/usr/bin/env python
import sys, re
from distutils.core import setup, Extension

version = "0.0.12"

if sys.version_info <= (2, 4):
    error = "ERROR: Bellatrix requires Python Version 2.5 or above...exiting."
    print >> sys.stderr, error
    sys.exit(1)


setup(name='bellatrix',
      version=version,
      long_description=open('README.txt').read(),
      description='Bellatrix is a comprehensive set of tools to automate the management of EC2 ami''s and instances.',

      keywords='ec2, ami, configuration, management, puppet',
      author='Adrian Deccico',
      author_email='adeccico@atlassian.com',
      url='https://bitbucket.org/adeccico/bellatrix',
      
      license='Apache License 2.0',
      
      packages=['bellatrix'],

      scripts=['bin/bewitch_ami',
               'bin/burn_instance',
               'bin/set_permissions',
               'bin/set_security',
               'bin/start_instance', 
               ],

      platforms = "Posix; MacOS X; Windows",
      
      #http://packages.python.org/distribute/setuptools.html#declaring-dependencies
      install_requires = ['boto==2.1.1'],

      #classifiers from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers = [
                     'Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: System Administrators',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     "Topic :: Internet",
                     'Topic :: System :: Software Distribution',
                     'Topic :: System :: Systems Administration',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Utilities',
                   ],
      )
