#!/usr/bin/python
'''
Set launch pemissions for an AMI
'''

import logging
import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib.bellatrix_util import *


class Run():
    def __init__(self, key, sec): 
        self._ec2 = Ec2lib(key, sec) 
        self.define_constants()

    def define_constants(self):
        """define class constants to access ami configs"""
        self.ACCOUNT_LEN = 12
    
    def getAccountPermissions(self, perm_file):
        """"Return list of accounts where new ami's will get execute permissions"""
        l = []
        with open(perm_file) as f:
             for line in f:
                 line=line.strip()
                 if len(line)==self.ACCOUNT_LEN:
                     l.append(line)
        logging.info("accounts from %s: %s" % (perm_file,l))
        return l
    
    def setPermissions(self, amis, permissions):
        self._ec2.setPermissionsToAmis(amis, permissions)
                     

def run(ami, permissions_file):
    r = Run(getKey(), getSecret())
    r.setPermissions(ami.split(","), r.getAccountPermissions(permissions_file))
    return 0


if __name__ == '__main__':
    sys.exit(run(*sys.argv[1]))
