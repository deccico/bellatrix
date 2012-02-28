'''
general utility functions
'''

import logging
import os
import time
import xml.dom.minidom


def getNodeValue(dom, nodename):
    """
    get 'myname' from a xml structure like this one when you call this method with 'name':
    <?xml version="1.0" encoding="UTF-8" ?>
    <root>
    <name>myname</name>
    </root>
    """
    return dom.getElementsByTagName(nodename).item(0).firstChild.nodeValue

def getDomFromXmlFile(xml_file):
    """
    parse an xml file and return its dom 
    """
    return xml.dom.minidom.parse(xml_file) 

def getValue(xml_file, value):
    """
    return the value from a xml tag

    this function will get 'myname' from a xml structure like this one when you call this method with 'name':
    <?xml version="1.0" encoding="UTF-8" ?>
    <root>
    <name>myname</name>
    </root>
    """
    return getNodeValue(getDomFromXmlFile(xml_file), value)

def getConfigDir(app_name):
    config_dir = None
    return config_dir
    
def getConfigFileContent(file_name, app_name):
    content = None
    return content

def getHome():
    return os.path.expanduser('~') or os.getenv('USERPROFILE') or os.getenv('HOME')

def getCurDir():
    return os.path.abspath(os.getcwd())

def getStringsFromFile(list_file):
    """"Return list from file ignoring blanks and comments"""
    l = []
    with open(list_file) as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and not line.startswith("#"):
                l.append(line)
    return l

def writeFile(file_name, content):
    with open(file_name, 'w') as out:
        out.write(content)

def importModule(module):
    dir_name = os.path.dirname(os.path.abspath(module))
    if len(dir_name) > 0 and os.path.sep in dir_name:
        #we change a normal path to a python module
        module = module.replace(os.path.sep, ".")
    return __import__(os.path.basename(module))


def waitForSSHReady(user, key, dns, TIME_OUT=300):
    ERR_CONNECTION_REFUSED = 65280 
    logging.info("waiting until host: " + dns + " is ready to receive ssh connections. Time out is: " + str(TIME_OUT) + " seconds...")
    tmp_file = "tmp"
    cmd = "ssh -o StrictHostKeyChecking=no -i %s %s@%s '%s' > %s" % (key, user, dns, "echo CONNECTION READY", tmp_file)
    step = 3
    result = ERR_CONNECTION_REFUSED
    while (result == ERR_CONNECTION_REFUSED and TIME_OUT > 0):
        TIME_OUT -= step
        time.sleep(step)
        logging.info("executing:%s " % cmd )
        result = os.system(cmd)
    if result !=  0:
        raise Exception("Sorry, but the instance never got ready for SSH connections")
    logging.info("Host %s is ready to receive ssh connections." % (dns))
