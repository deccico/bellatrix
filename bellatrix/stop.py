#!/usr/bin/python
'''
stop or terminate instances
'''
import logging

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util


class Finisher():
    def __init__(self, key, sec, message):
        self._ec2 = Ec2lib(key, sec)
        self.ALL_INSTANCES = "all"
        self.message = message

    def finish_instance(self, instance, finish_it):
        inst = []
        if self.ALL_INSTANCES == instance:
            inst = self._ec2.getInstances()
        else:
            inst = [self._ec2.getInstance(instance)]
            if inst[0] == None:
                raise Exception("Instance %s has not been found in this account." % instance)
        for i in inst:
            finish_it(i)
            logging.info("%s successfully %s." % (i, self.message) )
    
def stop(instance):
    f = Finisher(bellatrix_util.getKey(), bellatrix_util.getSecret(), "stopped")
    f.finish_instance(instance, f._ec2.stopInstance)
    return 0

def terminate(instance):
    f = Finisher(bellatrix_util.getKey(), bellatrix_util.getSecret(), "terminated")
    f.finish_instance(instance, f._ec2.terminateInstance)
    return 0
