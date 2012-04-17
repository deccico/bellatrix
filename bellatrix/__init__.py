#Constants

APP = "Bellatrix"
__version__ = '1.1.2'
description = "AWS EC2 magic utilities"

SECRET_FILE = "secret"
KEY_FILE = "key"
#path to the private key to connect to agents
PRIVATE_KEY_FILE = "ec2.pk"

OUT_TMP = "exec.tmp"


#---------------------------------------------------
#AWS constants

#shutdown behaviour
TERMINATE = "terminate"  
AMI_AVAILABLE = "available"
#running state for an ec2 instance
RUNNING = 16    
RUNNING_STRING = "running"
