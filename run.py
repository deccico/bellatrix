'''
Created on Aug 23, 2011

Starting point for the project.

ec2-upgraded is meant to automate the upgrade tasks to ec2 ami's.

this script needs "secret" and "key" files (with the correct EC2 credentials) in the current path

The idea is to:
    -start an instance
    -execute the correct upgrade steps  
    -burn the instance and save the new ami
'''

import logging
import os
import re
import pkgutil

APP="Bellatrix"
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    #filename='/tmp/ec2-killer.log',
                    filemode='a'
                    )

from boto.ec2.connection import EC2Connection
from ec2_lib import Ec2lib

#this script needs "secret" and "key" files in the current path
SECRET = open("secret").read().strip()
KEY = open("key").read().strip()
CONFIG_DIR = "./configs"  #todo get the path from the script
OUT_TMP = "exec.tmp"
PK = os.path.dirname(__file__) + os.path.sep + "ec2.pk"  #path to the private key to connect to agents


class Run():
    def __init__(self, key, sec): #todo move all the globals here
        self._ec2 = Ec2lib(KEY, SECRET) 

    def getEc2Instance(self, ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
        image = self._ec2.getImage(ami)  
        inst = self._ec2.startInstance(image, key_name, security_group, instance_type, APP, instance_initiated_shutdown_behavior="terminate")
        return inst

    def getConfigs(self):
        """get configurations from 'configs' directory"""
        import configs
        cfgpath = os.path.dirname(configs.__file__)
        return [name for _, name, _ in pkgutil.iter_modules([cfgpath])]
        
    def executeCommands(self, user, dns, key, commands):
        results = []
        for c in commands:
            cmd = "ssh -o StrictHostKeyChecking=no -i %s %s@%s '%s' > %s" % (key, user, dns, c, OUT_TMP)
            logging.info("executing: " + cmd)
            res = os.system(cmd)
            out = open(OUT_TMP).read()
            results.append([cmd, out, res])
            logging.info("result: " + str(res) + " output: " + out)
    
    def getAttr(self, module, attribute):
        """get attribute from module"""
        return eval(module + "." + attribute)
        
        
    def run(self):
        configs = self.getConfigs()
        for config in configs:
            logging.debug("processing: " + config)
            c = __import__(os.path.basename(CONFIG_DIR) + "." + config)
            mod = "c." + config + "."
            ami = eval(mod + "ami")
            commands =  eval(mod + "commands")
            user =  eval(mod + "user")
            inst = self.getEc2Instance(ami, "elasticbamboo", ["elasticbamboo"], 't1.micro')
            dns_name = self._ec2.getDNSName(inst)
            self._ec2.waitUntilInstanceIsReady(inst)
            r = self.executeCommands(user, inst.dns_name, PK, commands)
    

def run():
    r = Run(KEY, SECRET)
    r.run()
    
    #create a ec2 instance
    #inst = getEc2Instance("ami-a7a660ce", "elasticbamboo", ["elasticbamboo"], 't1.micro')
    #execute commands
    
    
    #get the configuration
    #start an instance
    #pick the right script
    #execute it
    #burn the image

if __name__ == '__main__':
    logging.info("starting ec2-upgrader")
    run()

