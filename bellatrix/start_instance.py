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

    def getEc2Instance(self, ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
        image = self._ec2.getImage(ami)  
        inst = self._ec2.startInstance(image, key_name, security_group, instance_type, APP, instance_initiated_shutdown_behavior="terminate")
        return inst

    def startInstance(self, ami, type, key_name, security_groups):
        inst = self.getEc2Instance(ami, key_name, security_groups.split(), type)
        dns_name = self._ec2.getDNSName(inst)
        self._ec2.waitUntilInstanceIsReady(inst)

def run(ami, type, key_name, security_groups):
    r = Run(bellatrix_util.getKey(), bellatrix_util.getSecret())
    r.startInstance(ami, type, key_name, security_groups)
    return 0


if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:]))
