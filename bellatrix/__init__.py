#Constants

APP = "Bellatrix"
__version__ = '0.0.27'
description = "AWS EC2 magic utilities"

CUR_DIR = os.path.abspath(os.getcwd())
PK = "ec2.pk" #path to the private key to connect to agents
if sys.platform != "cygwin": #for some reason ssh cygwin doesn't support the full path for the pk
    PK = CUR_DIR + os.path.sep + PK  
REPORTS_DIR = CUR_DIR + os.path.sep + "reports"

SECRET_FILE = "secret"
KEY_FILE = "key"

CONFIG_DIR = "./configs"  #todo get the path from the script
OUT_TMP = "exec.tmp"
