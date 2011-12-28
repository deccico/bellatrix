#!/usr/bin/python
'''
Modify security groups
'''

import logging
import os
import re
import pkgutil
import datetime
import sys

APP="Bellatrix"
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    #filename='out',
                    filemode='a'
                    )

from boto.ec2.connection import EC2Connection
from ec2_lib import Ec2lib

#this script needs "secret" and "key" files in the current path
SECRET = open("secret").read().strip()
KEY = open("key").read().strip()
CONFIG_DIR = "./configs"  #todo get the path from the script
OUT_TMP = "exec.tmp"
CUR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
PK = CUR_DIR + os.path.sep + "ec2.pk"  #path to the private key to connect to agents
REPORTS_DIR = CUR_DIR + os.path.sep + "reports"

class Run():
    def __init__(self, key, sec, app_name, pk): #todo move all the globals here
        self._ec2 = Ec2lib(KEY, SECRET) 
        self._app_name = app_name
        self.CMD_OK = 0
        self.define_constants()

    def define_constants(self):
        """define class constants to access ami configs"""
        self.AMIS = "amis"
        self.CMDS = "commands"
        self.USER = "user"
        self.BURN_OR_NOT = "burn_ami_at_the_end"
        self.SKIP_ME = "skip_me"
        self.ACCOUNT_LEN = 12
    
    #todo: move this to an util file
    def getStringsFromFile(self, list_file):
        """"Return list from file ignoring blanks and comments"""
        l = []
        with open(list_file) as f:
             for line in f:
                 line=line.strip()
                 if len(line) > 0 and not line.startswith("#"):
                     logging.debug("adding item: %s" % line)
                     l.append(line)
        return l
    
    def setSecurityGroupAuth(self, name, ports, cidrs):
        ports = self.getStringsFromFile(ports)
        cidrs = self.getStringsFromFile(cidrs)
        sg = self._ec2.getSecurityGroups(name)[0]
        self._ec2.revokeAllSecurityGroupRules(sg)
        for p in ports:
            for c in cidrs:
                self._ec2.authorizeSecurityGroup(sg, c, p)
            #allow same instances connection
            self._ec2.authorizeSecurityGroup(sg, None, p, sg)
                     

def run(args):
    logging.info("starting %s" % APP)
    security_group_name = args[1]
    r = Run(KEY, SECRET, APP, PK)
    r.setSecurityGroupAuth(name, CUR_DIR + os.path.sep + "ports_list", 
                           CUR_DIR + os.path.sep + "cidrs_list")
    logging.info("%s has finished" % APP)
    return 0

    

if __name__ == '__main__':
    sys.exit(run(sys.argv))



