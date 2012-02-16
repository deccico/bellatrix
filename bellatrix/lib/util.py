'''
general utility functions
'''

import os
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
             line=line.strip()
             if len(line) > 0 and not line.startswith("#"):
                 l.append(line)
    return l

def writeFile(filename, content):
    with open(filename, 'w') as out:
        out.write(content)
