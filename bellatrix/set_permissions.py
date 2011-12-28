#!/usr/bin/python
'''
Set launch pemissions for an AMI
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

    def checkPkFile(self, pk):
        if not os.path.isfile(pk): #todo add more validations (in a method)
            raise Exception("%s does not contain the private key file" % pk)
        
    def define_constants(self):
        """define class constants to access ami configs"""
        self.AMIS = "amis"
        self.CMDS = "commands"
        self.USER = "user"
        self.BURN_OR_NOT = "burn_ami_at_the_end"
        self.SKIP_ME = "skip_me"
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
                     

def run(args):
    logging.info("starting %s" % APP)
    ami = args[1]
    r = Run(KEY, SECRET, APP, PK)
    r.setPermissions(ami.split(","), r.getAccountPermissions("account_permissions"))
    logging.info("%s has finished" % APP)
    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv))

