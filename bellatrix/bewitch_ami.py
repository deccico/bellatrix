#!/usr/bin/python
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

import datetime
import logging
import os
import pkgutil
import re
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
CUR_DIR = os.path.abspath(os.getcwd())
PK = "ec2.pk" #path to the private key to connect to agents
if sys.platform != "cygwin": #for some reason ssh cygwin doesn't support the full path for the pk
    PK = CUR_DIR + os.path.sep + PK  
REPORTS_DIR = CUR_DIR + os.path.sep + "reports"

class Run():
    def __init__(self, key, sec, app_name, pk, reports): #todo move all the globals here
        self.checkPkFile(pk)
        self._ec2 = Ec2lib(KEY, SECRET) 
        self._app_name = app_name
        self.CMD_OK = 0
        self.define_constants()
        self.reports = reports
        if not os.path.isdir(reports):
            os.makedirs(reports)

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
        self.ALL_CONFIGS = "all"
        self.ACCOUNT_LEN = 12
    
    def getEc2Instance(self, ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
        image = self._ec2.getImage(ami)  
        inst = self._ec2.startInstance(image, key_name, security_group, instance_type, APP, instance_initiated_shutdown_behavior="terminate")
        return inst

    def getConfigs(self):
        """get configurations from 'configs' directory"""
        import configs
        cfgpath = os.path.dirname(configs.__file__)
        dir = os.path.basename(cfgpath)
        return [name for _, name, _ in pkgutil.iter_modules([cfgpath])]
        
    def executeCommands(self, user, dns, key, commands, config):
        results = []
        errors = []
        for c in commands:
            cmd = "ssh -o StrictHostKeyChecking=no -i %s %s@%s '%s' > %s" % (key, user, dns, c, OUT_TMP)
            logging.info("executing: " + cmd)
            res = os.system(cmd)
            out = open(OUT_TMP).read()
            cmd_res = [cmd, out, res, config]
            results.append(cmd_res)
            logging.info("result: " + str(res) + " output: " + out)
            #increment errors if necessary
            if res != 0:
                errors.append(cmd_res)
        logging.info("Commands executions: %s Errors: %s" % (len(commands), len(errors)))
        return results, errors

    def printErrors(self, errors):                
        logging.warning("The following commands failed its execution:")
        for e in errors:
            logging.warning("config: %s cmd: %s exit code: %s" % (e[3], e[0], e[2])) 
            logging.warning("last 500 chars output: %s" % e[1][-500:]) 
            
    def saveReport(self, results, config):                
        logging.info("Saving report")
        report_name = self.reports + os.path.sep + config + "-" + datetime.datetime.now().isoformat() + ".txt"
        with open(report_name, "w") as f:
            for r in results:
                f.write("res: %s cmd: %s out: %s \n" % (r[2], r[0], r[1])) 

    def _processConfig(self, amis, commands, user, burn_at_the_end):
        """execute a configuration, internal method of run"""
        amis_burned = []
        errors = [] 
        for ami in amis:
            config_name = ami[1]
            ami = ami[0]
            inst = self.getEc2Instance(ami, "elasticbamboo", ["elasticbamboo"], 't1.micro')
            dns_name = self._ec2.getDNSName(inst)
            self._ec2.waitUntilInstanceIsReady(inst)
            self._ec2.waitForConnectionReady(inst, user, PK, dns_name)
            r, e = self.executeCommands(user, inst.dns_name, PK, commands, config_name)
            self.saveReport(r, config_name)
            errors += e
            if burn_at_the_end:
                try:
                    new_ami = self._ec2.createImage(inst.id, config_name + "-" 
                                                    + datetime.datetime.now().isoformat(), "generated by " 
                                                    + self._app_name)
                    logging.info("ami: %s is being generated for configuration: %s" 
                                 % (new_ami, config_name))
                    amis_burned.append([new_ami, config_name])
                except:
                    logging.exception("Problem burning image: %s with instance: %s" % (config_name, inst.id))
            return amis_burned, errors

    def run(self, config):
        """execute a configuration"""
        amis_burned = []
        errors = []
        if config == self.ALL_CONFIGS:
            configs = self.getConfigs()
        else:
            configs = [config]
        sys.path = [CUR_DIR] + sys.path
        for cfg in configs:
            logging.info("processing: " + cfg + " in: " + os.getcwd())
            if config == self.ALL_CONFIGS:
                c = __import__(os.path.basename(CONFIG_DIR) + "." + cfg)
                mod = "c." + cfg + "."
            else:
                c = __import__(cfg)
                mod = "c."
            skip_me = eval(mod + self.SKIP_ME)
            if skip_me:
                logging.info("skipping execution of config: %s due to its configuration skip_me=true" % cfg)
                continue
            amis = eval(mod + self.AMIS)
            commands =  eval(mod + self.CMDS)
            user =  eval(mod + self.USER)
            burn_at_the_end = eval(mod + self.BURN_OR_NOT)
            a,e = self._processConfig(amis, commands, user, burn_at_the_end)
            amis_burned += a
            errors += e
        self.printErrors(errors)
        logging.info("total of ami's burned:%s" % len(amis_burned))
        for a in amis_burned:
            logging.info(str(a))
        return 0 if errors==0 else 1

    def getAccountPermissions(self, perm_file="account_permissions"):
        """"Return list of accounts where new ami's will get execute permissions"""
        l = []
        with open(perm_file) as f:
             for line in f:
                 line=line.strip()
                 if len(line)==self.ACCOUNT_LEN:
                     l.append(line)
        logging.info("accounts from %s: %s" % (perm_file,l))
        return l
    
    def setPermissionsToAmis(self, amis, permissions):
        self._ec2.setPermissionsToAmis(amis, permissions)

    
def run(args):
    logging.info("starting %s" % APP)
    r = Run(KEY, SECRET, APP, PK, REPORTS_DIR)
    config = r.ALL_CONFIGS if (len(args) < 2) else args[1]
    exit_code = r.run(config)
    logging.info("%s has finished" % APP)
    sys.exit(exit_code)

if __name__ == '__main__':
    run(sys.argv)

