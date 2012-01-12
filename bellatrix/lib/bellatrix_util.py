'''
Bellatrix utility functions
'''

import bellatrix
from bellatrix.lib.util import getCurDir

import os
import sys

def getConfigDir():
    return os.path.join(getHome(), "." + APP.lower())

def getConfigFile(path, file_name):
    if path == None:
        path = os.path.join(getConfigDir(), file_name) 
    return open(path)

def getSecret(path=None):
    return getConfigFile(path, bellatrix.SECRET_FILE)

def getKey(path=None):
    return getConfigFile(path, bellatrix.KEY_FILE)
    
def getPrivateKey(path=None):
    pk = getConfigFile(path, bellatrix.PRIVATE_KEY_FILE)
    if sys.platform != "cygwin": #for some reason ssh cygwin doesn't support the full path for the pk
        pk = getCurDir() + os.path.sep + pk  
    return pk 

def checkPkFile(pk):
    if not os.path.isfile(pk): #todo add more validations (in a method)
        raise Exception("%s does not contain the private key file" % pk)
    
REPORTS_DIR = CUR_DIR + os.path.sep + "reports"
CONFIG_DIR = "./configs"  #todo get the path from the script
OUT_TMP = "exec.tmp"


if not os.path.isdir(reports):
    os.makedirs(reports)
    