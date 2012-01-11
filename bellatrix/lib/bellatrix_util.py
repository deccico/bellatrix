'''
Bellatrix utility functions
'''

import bellatrix

import os

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
    