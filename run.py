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


def getEc2Instance(ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
    ec2 = Ec2lib(KEY, SECRET)
    image = ec2.getImage(ami)  
    inst = ec2.startInstance(image, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate")
    return inst

def run():
    #create a ec2 instance
    inst = getEc2Instance("ami-a7a660ce", "elasticbamboo", ["elasticbamboo"], 't1.micro')
    
    #get the configuration
    #start an instance
    #pick the right script
    #execute it
    #burn the image

if __name__ == '__main__':
    logging.info("starting ec2-upgrader")
    run()

