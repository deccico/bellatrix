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
    
    def _processConfig(self, amis, commands, user, key_name, hostname):
        """execute a configuration, internal method of run"""
        errors = []
        for ami in amis:
            config_name = ami[1]
            ami = ami[0]
            r, e = self.bewitch.executeCommands(user, hostname, key_name, commands, config_name)
            self.saveReport(r, config_name)
            errors += e
            if len(e) > 0:
                logging.warning("There were errors while executing the commands. Not burning the instance...")
            return errors

    def getVal(self, cfg, key, local_value):
        if local_value != None:
            return local_value
        else:
            return eval("cfg." + key)
    
    def provision(self, configuration, user, hostname, pk):
        """execute a configuration"""
        errors = []
        configs = os.path.splitext(configuration)[0]
        cfg = configs
        sys.path = [util.getCurDir()] + sys.path
        logging.info("processing: " + cfg + " in: " + os.getcwd())
        c = __import__(cfg)
        skip_me = self.getVal(c, self.SKIP_ME, None)
        if skip_me:
            logging.info("skipping execution of config: %s due to its configuration skip_me=true" % cfg)
        else:
            amis = self.getVal(c, self.bewitch.AMIS, None)
            commands = self.getVal(c, self.bewitch.CMDS, None)
            user =  self.getVal(c, self.bewitch.USER, user)
            key_name = self.getVal(c, self.bewitch.KEY_NAME, pk)
            errors = self._processConfig(amis, commands, user, key_name, hostname)
        self.printErrors(errors)
        return 0 if len(errors)==0 else 1

    
def run(configuration, user, hostname, pk):
    r = Provision('', '')
    exit_code = r.provision(configuration, user, hostname, pk)
    return exit_code

if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:])) 

