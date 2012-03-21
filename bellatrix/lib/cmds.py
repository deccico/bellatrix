""" 
Common utilities, meant to be used as 'building blocks'.
Every block has a different use, being possible in some cases to composite them. 

Every command is a simple function that returns the list of commands to be executed 
into a list of strings.
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
    """
    Return the "sudo apt-get install" command
    
    :type package: string
    :param package: The new package to install
    """
    return [apt_get_install_cmd + package]

def pip_install(package, prefix="sudo", verify=True, verification_command=None):
    """
    Install a Python package using pip.
    
    :type package: string
    :param package: The package to install.    

    :type prefix: string
    :param prefix: prefix of the pip command. It is 'sudo' by default.     

    :type verify: bool
    :param verify: True by default. If true, it will auto-generate a verification command to check the package has been installed correctly.      

    :type verification_command: string
    :param verification_command: None by default. If None, the verification command will be 'package --version' Otherwise it will execute the one provided in this argument.      
    """
    cmds = [prefix + " pip install " + package + " --upgrade"]
    if verification_command:
        cmds.append(package + " --version" if verification_command == None else verification_command)
    return cmds

def createVirtualEnv(env_name):
    """
    Generate a new Python virtual environment using virtualenv
    
    :type env_name: string
    :param env_name: Name of the new virtual environment.
    """
    return ["virtualenv --no-site-packages --clear " + env_name]

def executeInVirtualEnv(env, cmd):
    """
    Execute a command within a virtualenv environment
    
    :type env: str
    :param env: Name of the new virtual environment.

    :type cmd : list
    :param cmd: List of commands to be executed.
    """
    if type(cmd) == type(list()):
        cmd = flatCommands(cmd) 
    return ["source " + env + os.path.sep + "bin" + os.path.sep + "activate && " + cmd] 

def flatCommands(cmds):
    """
    Given a list of commands it will return a single one concatenated by '&&' so they will be executed in sequence until any of them fails.
    
    :type cmds: list
    :param cmds: List of strings that contains commands.
    
    :rtype: string
    :return: A single string with the commands concatenated.
    """
    cmd = ""
    ampersand = " && "
    #we need to get a single command so it works in the virtual environment
    for c in cmds:
        cmd += c + ampersand 
    cmd = cmd[:len(cmd) - len(ampersand)]   #cut last &&
    return cmd


def installPackageInVirtualEnv(env, package, verify=True, verification_command=None, prefix=""):
    """
    Install a Python package into a virtualenv.
    
    :type env: string
    :param env: Name of the virtual environment.

    :type package: string
    :param package: Package to be installed.

    :type verify: string
    :param verify: True by default. If true, it will auto-generate a verification command to check the package has been installed correctly.      

    :type verification_command: string
    :param verification_command: None by default. If None, the verification command will be 'package --version' Otherwise it will execute the one provided in this argument.      

    :type prefix: string
    :param prefix: Prefix of the pip command. It is 'sudo' by default.     
    """
    cmds = pip_install(package, prefix, verify, verification_command) 
    cmd = flatCommands(cmds)
    return executeInVirtualEnv(env, cmd) 

def install_pip():
    """
    Install pip using apt-get install.
    """
    #we need to upgrade pip package using pip itself
    return apt_get_install("python-pip") + pip_install("pip")    
               
def apt_get_update():
    """
    Executes apt-get update.
    """
    return [
            apt_get_and_options + "update"
            ]

def install_nginx():
    """
    Install Nginx in Ubuntu using the repo they provide as described in http://wiki.nginx.org/Install#Ubuntu_PPA
    """
    return ["sudo add-apt-repository ppa:nginx/stable -y"] + apt_get_update() + apt_get_install("nginx")
                
def create_django_project(project_name, dir_name="." + os.path.sep):                
    """
    Creates a Django project.
    
    :type project_name: string
    :param project_name: Name of the Django project.

    :type dir_name: string
    :param dir_name: Directory where the Django project needs to be executed. By default is the current directory.  
    """
    return ["cd " + dir_name + " && rm -rf " + project_name + " && django-admin.py startproject " + project_name]

def wget(url, dest=None):
    """
    Downloads a web resource using wget.
    
    :type url: string
    :param url: Url to download.

    :type dest: string
    :param dest: Optional. Destination in our machine of the downloaded resource.
    """
    return ["wget --no-check-certificate " + url + ("" if dest == None else " -O " + dest)]

def sudo(cmds):
    """
    Execute a list of commands using sudo.
    
    :type cmds: list
    :param cmds: List of commands.
    """
    for i in range(len(cmds)):
        cmds[i] = "sudo " + cmds[i]
    return cmds

def chmod(mode, file_name, options=""):
    """
    Applies the chmod command.
    
    :type mode: string
    :param mode: New mode of the destination. Typical examples are: a+r to give read permissions to everyone, a+rx to give execution and read permissions to any user, etc.

    :type file_name: string
    :param file_name: Destination of the new mode.

    :type options: string
    :param options: Optional set of parameters for this command.   
    """
    return ["chmod " + options + " " + mode + " " + file_name]    
    
def mkdir(directory):
    """
    Created a new directory. "-p" flag is used so the command generates the same result regardless whether the directory exists or not. 
    
    :type directory: string
    :param directory: directory to be created.
    """
    return ["mkdir -p " + directory]    

def createSoftLink(src, dest):
    """
    Creates a new soft link.
    
    :type src: string
    :param Src: Source file or directory.

    :type dest: string
    :param Dest: Name of the soft link.
    """
    return ["ln -f -s %s %s" % (src, dest)]    

def copy(src, dest):
    """
    Copy a file using -f so it doesn't fail if the destination exists.

    :type src: string
    :param src: Source file.

    :type dest: string
    :param dest: File destination.
    """
    return ["cp -f %s %s" % (src, dest)]    

#def scp(src, dest):
#    return [
#            "mkdir -p %s" % src,
#            {cmd:"scp -o StrictHostKeyChecking=no -i %(key)s -r *.sh Rakefile manifests/ features/ modules/ %(user)s@%(dns)s:" 
#             + "%s" % src  
#             + ";let RET=$?;exit $RET"} 
#            ]
