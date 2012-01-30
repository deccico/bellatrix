#!/usr/bin/python
'''
Upload files to S3 
'''

from ec2_lib import Ec2lib
from bellatrix.lib.bellatrix_util import *


class Run():
    def __init__(self, key, sec):
        self._ec2 = Ec2lib(key, sec)
    
    def uploadToS3(self, source, bucket, acl="public-read"):
        self._ec2.uploadToS3(source, bucket, acl)
        
    
def run(source, bucket, acl):
    r = Run(getKey(), getSecret())
    exit_code = r.uploadToS3(source, bucket, acl)
    return exit_code

if __name__ == '__main__':
    sys.exit(run(sys.argv[1], sys.argv[2], sys.argv[3])) 

