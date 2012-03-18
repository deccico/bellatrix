""" 
Common utilities, meant to be used as 'building blocks'.
Every block has a different utility, being possible in some cases to composite them. 

Every command is a simple function that returns the commands to be executed into a list of strings.
If any of the commands fails, the execution will be interrupted. 
It's convenient that you add a small test at the very end of each set. 

For example:

def install_pip():
    return [
            "touch new_file",
            "cat new_file",
            ] 
               
It's an example of a single-purposed operation that performs a test at the end. 
Should something happened to the operation, 'cat new_file' will fail. 
Additionally you will be able to verify the content of the file in the logging output.               
"""

import os

#CONSTANTS
#http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=422427
apt_prefix = "export PATH=$PATH:/sbin:/usr/sbin:/usr/local/sbin;export TERM=linux; "
apt_get_and_options = "sudo /usr/bin/apt-get -q -y -o DPkg::Options::=--force-confold --fix-missing " 
apt_install = apt_get_and_options + "install "
apt_get_install_cmd = apt_prefix + apt_install 


def apt_get_install(package):
    return [apt_get_install_cmd + package]

def pip_install(package, prefix="sudo", verify=True, verification_command=None):
    cmds = [prefix + " pip install " + package + " --upgrade"]
    if verification_command:
        cmds.append(package + " --version" if verification_command == None else verification_command)
    return cmds

def createVirtualEnv(env_name):
    return ["virtualenv --no-site-packages --clear " + env_name]

def executeInVirtualEnv(env, cmd):
    if type(cmd) == type(list()):
        cmd = flatCommands(cmd) 
    return ["source " + env + os.path.sep + "bin" + os.path.sep + "activate && " + cmd] 

def flatCommands(cmds):
    """Given a list of commands returns a single one"""
    cmd = ""
    ampersand = " && "
    #we need to get a single command so it works in the virtual environment
    for c in cmds:
        cmd += c + ampersand 
    cmd = cmd[:len(cmd) - len(ampersand)]   #cut last &&
    return cmd


def installPackageInVirtualEnv(env, package, verify=True, verification_command=None, prefix=""):
    cmds = pip_install(package, prefix, verify, verification_command) 
    cmd = flatCommands(cmds)
    return executeInVirtualEnv(env, cmd) 

def install_pip():
    #we need to upgrade pip package using pip itself
    return apt_get_install("python-pip") + pip_install("pip")    
               
def apt_get_update():
    return [
            apt_get_and_options + "update"
            ]

#from: http://wiki.nginx.org/Install#Ubuntu_PPA
def install_nginx():
    return ["sudo add-apt-repository ppa:nginx/stable -y"] + apt_get_update() + apt_get_install("nginx")
                
def create_django_project(project_name, dir_name="." + os.path.sep):                
    return ["cd " + dir_name + " && rm -rf " + project_name + " && django-admin.py startproject " + project_name]

def wget(url, dest=None):
    return ["wget --no-check-certificate " + url + ("" if dest == None else " -O " + dest)]

def sudo(cmds):
    for i in range(len(cmds)):
        cmds[i] = "sudo " + cmds[i]
    return cmds

def chmod(mode, file_name, options=""):
    return ["chmod " + options + " " + mode + " " + file_name]    
    
def mkdir(directory):
    return ["mkdir -p " + directory]    

def createSoftLink(src, dest):
    return ["ln -f -s %s %s" % (src, dest)]    

def copy(src, dest):
    return ["cp -f %s %s" % (src, dest)]    

#def scp(src, dest):
#    return [
#            "mkdir -p %s" % src,
#            {cmd:"scp -o StrictHostKeyChecking=no -i %(key)s -r *.sh Rakefile manifests/ features/ modules/ %(user)s@%(dns)s:" 
#             + "%s" % src  
#             + ";let RET=$?;exit $RET"} 
#            ]
