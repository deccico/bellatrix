'''
Bellatrix utility functions
'''

import bellatrix
from bellatrix.lib.util import *

import os
import sys

def getConfigDir():
    return os.path.join(getHome(), "." + bellatrix.APP.lower())

def getConfigFile(path, file_name, description=None):
    if path == None:
        path = os.path.join(getConfigDir(), file_name) 
    if not os.path.isfile(path):
        raise Exception(
                          """Error getting configuration file. \n """ 
                          """%s is looking for the file %s and can not find it.\n """
                          """Please generate it and try again. %s""" \
                          % (bellatrix.APP, path, "" if description is None else description))
    return open(path)

def getSecret(path=None):
    return getConfigFile(path, bellatrix.SECRET_FILE, \
                         """Secret Access Key is part of your AWS security credentials. """
                         """Please sign into https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key"""
                         """in order to get your keys.""")

def getKey(path=None):
    return getConfigFile(path, bellatrix.KEY_FILE, \
                         """The Access Key Id is part of your AWS security credentials. """
                         """Please sign into https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key"""
                         """in order to get your keys.""")
    
def getPrivateKey(path=None):
    pk = getConfigFile(path, bellatrix.PRIVATE_KEY_FILE)
    if sys.platform != "cygwin": #for some reason ssh cygwin doesn't support the full path for the pk
        pk = getCurDir() + os.path.sep + pk  
    return pk 

def checkPkFile(pk):
    if not os.path.isfile(pk): #todo add more validations (in a method)
        raise Exception("%s does not contain the private key file" % pk)

def getReportsDir():    
    reportsDir = getCurDir() + os.path.sep + "reports" 
    if not os.path.isdir(reportsDir):
        os.makedirs(reportsDir)
    return reportsDir