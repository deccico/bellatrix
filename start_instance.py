#!/usr/bin/python
'''
this needs a good refactor
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
    def __init__(self, key, sec, app_name, pk, ami, type): #todo move all the globals here
        self.checkPkFile(pk)
        self._ec2 = Ec2lib(KEY, SECRET) 
        self._app_name = app_name
        self.CMD_OK = 0
        self.define_constants()
        self.startInstance(ami, type)

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
    
    def getEc2Instance(self, ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
        image = self._ec2.getImage(ami)  
        inst = self._ec2.startInstance(image, key_name, security_group, instance_type, APP, instance_initiated_shutdown_behavior="terminate")
        return inst

    def startInstance(self, ami, type):
        inst = self.getEc2Instance(ami, "elasticbamboo", ["elasticbamboo"], type)
        dns_name = self._ec2.getDNSName(inst)
        self._ec2.waitUntilInstanceIsReady(inst)

def run(ami, type):
    r = Run(KEY, SECRET, APP, PK, ami, type)

if __name__ == '__main__':
    logging.info("starting %s" % APP)
    ami = sys.argv[1]
    if len(sys.argv) < 3:
        type = 'm1.large'
    else:
        type = sys.argv[2]
    run(ami, type)
    logging.info("%s has finished" % APP)

