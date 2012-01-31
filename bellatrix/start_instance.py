#!/usr/bin/python
'''
this needs a good refactor
'''

import logging
import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util

class Run():
    def __init__(self, key, sec, ami, type): #todo move all the globals here
        self._ec2 = Ec2lib(key, sec) 
        self.startInstance(ami, type)

    def getEc2Instance(self, ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
        image = self._ec2.getImage(ami)  
        inst = self._ec2.startInstance(image, key_name, security_group, instance_type, APP, instance_initiated_shutdown_behavior="terminate")
        return inst

    def startInstance(self, ami, type):
        inst = self.getEc2Instance(ami, "elasticbamboo", ["elasticbamboo"], type)
        dns_name = self._ec2.getDNSName(inst)
        self._ec2.waitUntilInstanceIsReady(inst)

def run(args):
    ami = args[1]
    if len(args) < 3:
        type = 'm1.large'
    else:
        type = args[2]
    r = Run(KEY, SECRET, APP, ami, type)
    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv))

