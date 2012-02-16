#!/usr/bin/python
'''
stop or terminate instances
'''

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util


class Finisher():
    def __init__(self, key, sec):
        self._ec2 = Ec2lib(key, sec)
        self.ALL_INSTANCES = "all"

    def finish_instance(self, instance, finish_it):
        for i in (self._ec2.getInstances() if self.ALL_INSTANCES == instance else [instance]):
            finish_it(i)
    
def stop(instance):
    f = Finisher(bellatrix_util.getKey(), bellatrix_util.getSecret())
    f.finish_instance(instance, f._ec2.stop)
    return 0

def terminate(instance):
    f = Finisher(bellatrix_util.getKey(), bellatrix_util.getSecret())
    f.finish_instance(instance, f._ec2.terminate)
    return 0
