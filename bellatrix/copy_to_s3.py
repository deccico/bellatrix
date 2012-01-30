#!/usr/bin/python
'''
Upload files to S3 
'''

import bellatrix
from bellatrix.lib.util import *
from bellatrix.lib.bellatrix_util import *

from boto.ec2.connection import EC2Connection
from ec2_lib import Ec2lib

class Run():
    def __init__(self, key, sec):
        self._ec2 = Ec2lib(key, sec)
    
    def uploadToS3(self, bucket, source):
        self._ec2.uploadToS3(bucket, source, source, acl="public")
        
         

    
def run(configuration=None):
    r = Run(getKey(), getSecret())

    exit_code = r.copy(config)
    logging.info("%s has finished" % os.path.basename(__file__))
    return exit_code

if __name__ == '__main__':
    sys.exit(run(sys.argv))

