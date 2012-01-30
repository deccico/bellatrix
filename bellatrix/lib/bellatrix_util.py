'''
Bellatrix utility functions
'''

import bellatrix
import bellatrix.lib.util

import os
import sys

def getConfigDir():
    return os.path.join(bellatrix.lib.util.getHome(), "." + bellatrix.APP.lower())

def getConfigFile(path, file_name, get_content, description=None):
    if path == None:
        path = os.path.join(getConfigDir(), file_name) 
    if not os.path.isfile(path):
        sys.tracebacklimit = 0 #we don't need the stack trace in this particular case.
        raise Exception(
                          """\n\n -------------------------- \n""" 
                          """Error getting configuration file. \n""" 
                          """%s is looking for the file %s and can not find it.\n"""
                          """Please generate it and try again. %s""" \
                          % (bellatrix.APP, path, "" if description is None else description))
    if get_content:
        return open(path).read()
    else:
        return path

def getSecret(path=None):
    return getConfigFile(path, bellatrix.SECRET_FILE, True, \
                         """The file should contain your 'secret access key' (a string with an approximate length of 50 characters) and is part of your AWS security credentials.\n"""
                         """Please sign into: \nhttps://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key\n"""
                         """in order to get your keys.""")

def getKey(path=None):
    return getConfigFile(path, bellatrix.KEY_FILE, True, \
                         """The file should contain your 'access key id' (something like AKIAIU**************) and is part of your AWS security credentials.\n"""
                         """Please sign into: \nhttps://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key\n"""
                         """in order to get your keys.""")
    
def getPrivateKey(path=None):
    pk = getConfigFile(path, bellatrix.PRIVATE_KEY_FILE, False, \
                       """This file is the private key to use in order to connect to your instance.\n"""
                       """You should have your key-pair already specified. For more details, please refer to:\n"""
                       """http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/generating-a-keypair.html"""
                       )
    #TODO: check what happens when executing this withing cygwin. Probably we shouldn't worry after moving to Fabric
    #if sys.platform != "cygwin": #for some reason ssh cygwin doesn't support the full path for the pk
    #    pk = bellatrix.lib.util.getCurDir() + os.path.sep + pk  
    return pk 

def checkPkFile(pk):
    if not os.path.isfile(pk): #todo add more validations (in a method)
        raise Exception("%s does not contain the private key file" % pk)

def getReportsDir():    
    reportsDir = bellatrix.lib.util.getCurDir() + os.path.sep + "reports" 
    if not os.path.isdir(reportsDir):
        os.makedirs(reportsDir)
    return reportsDir

