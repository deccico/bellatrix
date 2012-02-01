#!/usr/bin/python
'''
this needs a good refactor
'''

import logging
import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util

class Run():
    def __init__(self, key, sec): 
        self._ec2 = Ec2lib(key, sec) 

    def startInstance(self, ami, type, key_name, security_groups):
        Ec2lib.startInstance(ami, type, key_name, security_groups)

def run(ami, type, key_name, security_groups):
    r = Run(bellatrix_util.getKey(), bellatrix_util.getSecret())
    r.startInstance(ami, type, key_name, security_groups)
    return 0


if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:]))
