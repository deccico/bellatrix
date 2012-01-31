#!/usr/bin/python
'''
Modify security groups
'''

import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import util
from bellatrix.lib import bellatrix_util



class Run():
    def __init__(self, key, sec):
        self._ec2 = Ec2lib(key, sec) 

    def setSecurityGroupAuth(self, name, ports, cidrs):
        ports = util.getStringsFromFile(ports)
        cidrs = util.getStringsFromFile(cidrs)
        sg = self._ec2.getSecurityGroups(name)[0]
        self._ec2.revokeAllSecurityGroupRules(sg)
        for p in ports:
            for c in cidrs:
                self._ec2.authorizeSecurityGroup(sg, c, p)
            #allow same instances connection
            self._ec2.authorizeSecurityGroup(sg, None, p, sg)
                     

def run(args, security_group_name, ports_file, cidrs_file):
    r = Run(bellatrix_util.getKey(), bellatrix_util.getSecret())
    r.setSecurityGroupAuth(security_group_name, ports_file, cidrs_file)
    return 0

    

if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:]))



