#!/usr/bin/python
'''
Given a running machine with ssh, apply a configuration 
'''

import logging
import os
import sys

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util
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
            r, e = self.executeCommands(user, inst.dns_name, self.pk, commands, config_name)
            self.saveReport(r, config_name)
            errors += e
            if len(e) > 0:
                logging.warning("There were errors while executing the commands. Not burning the instance...")
            return errors

    def run(self, config):
        """execute a configuration"""
        amis_burned = []
        errors = []
        if config == self.ALL_CONFIGS:
            configs = self.getConfigs()
        else:
            configs = [os.path.splitext(config)[0]]
        sys.path = [bellatrix.lib.util.getCurDir()] + sys.path
        for cfg in configs:
            logging.info("processing: " + cfg + " in: " + os.getcwd())
            if config == self.ALL_CONFIGS:
                c = __import__(os.path.basename(self.CONFIG_DIR) + "." + cfg)
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
            a,e = self._processConfig(amis, commands, user, burn_at_the_end, eval(mod + self.KEY_NAME), 
                                      eval(mod + self.SECURITY_GROUPS), eval(mod + self.INSTANCE_TYPE))
            amis_burned += a
            errors += e
        self.printErrors(errors)
        logging.info("total of ami's burned:%s" % len(amis_burned))
        for a in amis_burned:
            logging.info(str(a))
        return 0 if len(errors)==0 else 1

    
def run(configuration=None):
    r = Provision(bellatrix_util.getKey(), bellatrix_util.getSecret())
    config = r.ALL_CONFIGS if (not configuration) else configuration
    exit_code = r.provision(config)
    return exit_code

if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:])) 

