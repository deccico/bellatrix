#!/usr/bin/python
'''
List current EC2 instances
'''

from bellatrix.lib.ec2_lib import Ec2lib
from bellatrix.lib import bellatrix_util
import bellatrix

import logging

class Lister():
    def __init__(self, key, sec):
        self._ec2 = Ec2lib(key, sec)
        self.space = " | "
        self.attributes = ['architecture', 'block_device_mapping', 'connection', 'dns_name',\
                           'group_name', 'groups', 'hypervisor', 'image_id', 'instance_type',\
                           'ip_address', 'kernel', 'key_name', 'launch_time',\
                           'private_dns_name', 'private_ip_address', 'public_dns_name', 'region',\
                           'root_device_name', 'root_device_type', 'shutdown_state',\
                           'spot_instance_request_id', 'state', 'state_code', 'state_reason',\
                           'subnet_id', 'tags', 'virtualizationType', 'vpc_id']

    def printInstancesInformation(self, instances):
        total = 0
        running = 0
        for i in instances:
            msg = str(i)
            for a in self.attributes:
                try:
                    attr = getattr(i, a)
                    msg += self.space + a + ":" + attr 
                except:
                    logging.debug("Warning. I couldn't find the attribute %s in instance %s" % (a, str(i)))
            print msg
            total += 1
            if i.state == bellatrix.RUNNING_STRING:
                running += 1 
            print ""
        print "Running instances (you pay for them):%s" % running
        print "Total instances:%s" % total

    def list(self):
        logging.info("Getting instances information... (this operation usually takes some seconds)")
        instances = self._ec2.getAllInstances() 
        if len(instances)==0:
            logging.info("There are no EC2 instances in your account.")
        else:
            self.printInstancesInformation(instances)
    

def list():
    l = Lister(bellatrix_util.getKey(), bellatrix_util.getSecret())
    l.list()
    return 0
