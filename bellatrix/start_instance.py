#!/usr/bin/python
'''
this needs a good refactor
'''

import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util
from bellatrix.lib import util

class Run():
    def __init__(self, key, sec): 
        self._ec2 = Ec2lib(key, sec) 
        self.out_file = bellatrix_util.getOutFile(__file__)
        

    def startInstance(self, ami, instance_type, key_name, security_groups):
        inst, dns_name = self._ec2.startInstance(ami, instance_type, key_name, security_groups)
        util.writeFile(self.out_file, inst.id + "," + dns_name)
        

def run(ami, instance_type, key_name, security_groups):
    r = Run(bellatrix_util.getKey(), bellatrix_util.getSecret())
    r.startInstance(ami, instance_type, key_name, security_groups)
    return 0


if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:]))
