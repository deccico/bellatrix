#!/usr/bin/python
'''
Given a running machine with ssh, apply a configuration 
'''

import logging
import os
import sys

from bellatrix.lib import bellatrix_util
from bellatrix.lib import util
import bellatrix.bewitch_ami


class Provision(bellatrix.bewitch_ami.Bewitch):
    def __init__(self,  key, sec, app_name, pk, reports):
        #we cheat on the pk so Bewitch doesn't complain
        bellatrix.bewitch_ami.Bewitch.__init__(self, key, sec, app_name, pk, reports)
    
    def _processConfig(self, amis, commands, user, key_name, hostname):
        """execute a configuration, internal method of run"""
        errors = []
        for ami in amis:
            config_name = ami[1]
            ami = ami[0]
            r, e = self.executeCommands(user, hostname, key_name, commands, config_name)
            self.saveReport(r, config_name)
            errors += e
            if len(e) > 0:
                logging.warning("There were errors while executing the commands. Not burning the instance...")
            return errors

    def getVal(self, cfg, module_name, key, local_value):
        logging.debug("getting value from module:%s key:%s local value:%s module data:%s" \
                     % (module_name, key, local_value, dir(cfg)))
        if local_value != None:
            return local_value
        else:
            key = "cfg." + module_name + "." + key
            return eval(key)
    
    def provision(self, configuration, user, hostname, pk):
        """execute a configuration"""
        errors = []
        configs = os.path.splitext(configuration)[0]
        cfg = configs
        sys.path = [util.getCurDir()] + sys.path
        logging.info("processing: " + cfg + " in: " + os.getcwd())
        module_name = os.path.basename(cfg) 
        c = util.importModule(cfg)
        skip_me = self.getVal(c, module_name, self.SKIP_ME, None)
        if skip_me:
            logging.info("skipping execution of config: %s due to its configuration skip_me=true" % cfg)
        else:
            amis = self.getVal(c, module_name, self.AMIS, None)
            commands = self.getVal(c, module_name, self.CMDS, None)
            user =  self.getVal(c, module_name, self.USER, user)
            key_name = self.getVal(c, module_name, self.KEY_NAME, pk)
            errors = self._processConfig(amis, commands, user, key_name, hostname)
        self.printErrors(errors)
        return 0 if len(errors)==0 else 1

    
def run(configuration, user, hostname, pk):
    r = Provision('', '', bellatrix.APP, __file__, bellatrix_util.getReportsDir())
    exit_code = r.provision(configuration, user, hostname, pk)
    return exit_code

if __name__ == '__main__':
    sys.exit(run(*sys.argv[1:])) 

