#!/usr/bin/python
'''
Given a running machine with ssh, apply a configuration 
'''

import logging
import os
import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util
from bellatrix.lib import util
import bellatrix.bewitch_ami


class Provision():
    def __init__(self, key, sec):
        self._ec2 = Ec2lib(key, sec)
        self.bewitch = bellatrix.bewitch_ami.Run(key, sec, bellatrix.APP, \
                                                 bellatrix_util.getPrivateKey(), \
                                                 bellatrix_util.getReportsDir())
    
    def provision(self, config):
        exit_code = 0
        return exit_code

    def _processConfig(self, amis, commands, user, key_name):
        """execute a configuration, internal method of run"""
        errors = []
        for ami in amis:
            config_name = ami[1]
            ami = ami[0]
            r, e = self.executeCommands(user, dns_name, pk, commands, config_name)
            self.saveReport(r, config_name)
            errors += e
            if len(e) > 0:
                logging.warning("There were errors while executing the commands. Not burning the instance...")
            return errors

    def run(self, config):
        """execute a configuration"""
        amis_burned = []
        errors = []
        configs = os.path.splitext(config)[0]
        cfg = configs
        sys.path = [util.getCurDir()] + sys.path
        logging.info("processing: " + cfg + " in: " + os.getcwd())
        c = __import__(cfg)
        mod = "c."
        skip_me = eval(mod + self.SKIP_ME)
        if skip_me:
            logging.info("skipping execution of config: %s due to its configuration skip_me=true" % cfg)
        else:
            amis = eval(mod + self.AMIS)
            commands =  eval(mod + self.CMDS)
            user =  eval(mod + self.USER)
            a,e = self._processConfig(amis, commands, user, eval(mod + self.KEY_NAME), 
                                      eval(mod + self.SECURITY_GROUPS), eval(mod + self.INSTANCE_TYPE))
            amis_burned += a
            errors += e
        self.printErrors(errors)
        return 0 if len(errors)==0 else 1

    
def run(configuration):
    r = Provision(bellatrix_util.getKey(), bellatrix_util.getSecret())
    exit_code = r.provision(configuration)
    return exit_code

if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:])) 

