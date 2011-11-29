""" common utilities, meant to be used as build blocks by configs. 

Please, keep every block independent from the others. 
"""

#special cases are not special enough... PEP20
skip_me = True
amis = []
user = ""

def changeCommands(cmds, old_value, new_value):
    list = cmds
    for i in range(len(list)):
        list[i] = list[i].replace(old_value, new_value)
    return list

upgrade_ubuntu = ["sudo apt-get update -y",
                  "sudo apt-get upgrade -y",
                  ]

kill_java_python = ["killall python -w -v",
                    "killall java -w -v",
                    ]

clean_home = ["rm -rf $HOME/*;ls $HOME"]

def getCreateRcLocal(user, home="$HOME"):
    rc_local = "rc.local"
    create_rc_local = ["echo \#\!/bin/sh -e > %s" % rc_local,
                       "echo ulimit -n 8192 >> %s" % rc_local,
                       "echo cd %s >> %s" % (home, rc_local),
                       "echo su -c %s/igniter.py - %s >> %s" % (home, user, rc_local),
                       "sudo rm /etc/rc.local",
                       "chmod a+x %s" % rc_local,
                       "sudo cp %s /etc/rc.local" % rc_local,
                       "cat /etc/rc.local",
                       ]
    return create_rc_local

deploy_igniter = ["wget https://s3.amazonaws.com/bamboo-ec2-igniter/igniter.py",
                  "chmod a+x igniter.py;ls -la igniter.py"
                  ]

jdk = "jdk-6u26-linux-x64.bin"
java_dir = "jdk1.6.0_26"
install_jdk_16_26 = [
                     "wget https://s3.amazonaws.com/bamboo-ec2/%s" % jdk,
                     "chmod a+x %s" % jdk,
                     "echo |./%s >out_jdk 2>&1" % jdk,
                     "cat out_jdk",
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv %s /opt/java/sdk/" % java_dir,
                     "/opt/java/sdk/%s/bin/java -version > out;cat out" % java_dir
                     ]

jdk = "jdk-6u27-linux-x64.bin"
java_dir = "jdk1.6.0_27"
install_jdk_16_27 = [
                     "wget https://s3.amazonaws.com/bamboo-ec2/%s" % jdk,
                     "chmod a+x %s" % jdk,
                     "echo |./%s >out_jdk 2>&1" % jdk,
                     "cat out_jdk",
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv %s /opt/java/sdk/" % java_dir,
                     "/opt/java/sdk/%s/bin/java -version" % java_dir
                     ]

jdk = "jdk-7-linux-x64.tar.gz"
java_dir = "jdk1.7.0"
install_jdk_17_00  = [
                     "wget https://s3.amazonaws.com/bamboo-ec2/%s" % jdk,
                     "tar -xvzf %s" % jdk,
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv %s /opt/java/sdk/" % java_dir,
                     "/opt/java/sdk/%s/bin/java -version" % java_dir
                     ]

install_bamboo_assembly =[
                           "wget https://s3.amazonaws.com/bamboo-ec2-jbac/jbac_agent.zip",
                           "unzip -o jbac_agent.zip",
                           "cp bamboo-elastic-agent/bin/bamboo-ec2-metadata $HOME/bamboo-ec2-metadata.exe",
                           "ls $HOME/bamboo-ec2-metadata.exe"
                           ]

out = "$HOME/.s3cfg"
install_s3_cmd = [
                  "wget https://s3.amazonaws.com/bamboo-ec2/s3cmd.zip",
                  "unzip -o -d $HOME/s3cmd s3cmd.zip",
                  "cd $HOME/s3cmd/s3cmd;sudo python setup.py install",
                  "echo [default] > %s" % out,
                  "echo access_key = AKIAJ55SDWUCH2HHBUCA >> %s" % out,
                  "echo secret_key = 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 >> %s" % out,
                  "cat %s" % out
                  ]
out = "/home/oracle/.bash_profile"
oracle_bash_profile = [
                  "rm %s" % out,     
                  "echo # Get the aliases and functions > %s" % out,
                  "echo 'if [ -f ~/.bashrc ]; \then' >> %s" % out,
                  "echo   . \~/.bashrc >> %s" % out,
                  "echo                >> %s" % out,
                  "echo \# User specific environment and startup programs >> %s" % out,
                  "echo JAVA_HOME=/usr/java/jdk1.6.0_24 >> %s" % out,
                  "echo M2_HOME=/opt/apache-maven-2.1.0 >> %s" % out,
                  "echo export M2_HOME >> %s" % out,
                  "echo PATH=$PATH:$HOME/bin:/$M2_HOME/bin >> %s" % out,
                  "echo PATH=$PATH:$HOME/bin >> %s" % out,
                  "echo                >> %s" % out,
                  "echo export PATH    >> %s" % out,
                  "echo                >> %s" % out,
                  "echo  \## Oracle Setup \## >> %s" % out,
                  "echo umask 022  >> %s" % out,
                  "echo ORACLE_BASE=/u01/app >> %s" % out,
                  "echo ORACLE_HOME=/u01/app/oracle/product/11.2.0/db_1 >> %s" % out,
                  "echo \#JAVA_HOME=${ORACLE_HOME}/jdk >> %s" % out,
                  "echo 'PS1=\"`whoami`@`uname -n`:[\$PWD]`echo -e '\n\$ '`\"' >> %s" % out,
                  "echo PATH=${ORACLE_HOME}/bin:${JAVA_HOME}/bin:$M2_HOME/bin:$PATH >> %s" % out,
                  "echo EDITOR=vi               >> %s" % out,
                  "echo set -o vi               >> %s" % out,
                  "echo                >> %s" % out,
                  "echo export ORACLE_BASE ORACLE_HOME PS1 PATH EDITOR >> %s" % out,
                  "echo export ORACLE_HOSTNAME=localhost               >> %s" % out,
                  "echo export ORACLE_SID=beacsid               >> %s" % out,
                  "echo export JAVA_HOME               >> %s" % out,
                  "echo                >> %s" % out,
                  "chown oracle:oinstall %s" % out,
                  "ls -la %s" % out,
                  "cat %s" % out,
                  ]

out = "/home/oracle/.bash_profile"
ora_bash_profile_check = [
                  "ls -la %s" % out,
                  "cat %s" % out,
                  ]

out = "/u01/app/oracle/product/11.2.0/db_1/network/admin/listener.ora"
oracle_listener = [
                   "rm %s" % out,     
                   "echo ls -la %s" % out,
                   "echo SID_LIST_LISTENER =               >> %s" % out,
                   "echo \(SID_LIST = >> %s" % out,
                   "echo   \(SID_DESC = >> %s" % out,
                   "echo     \(SID_NAME = beacsid\)  >> %s" % out,
                   "echo      \(ORACLE_HOME = /u01/app/oracle/product/11.2.0/db_1\) >> %s" % out,
                   "echo      \(PROGRAM = extproc\) >> %s" % out,
                   "echo    \) >> %s" % out,
                   "echo   \(SID_DESC= >> %s" % out,
                   "echo         \(GLOBAL_DBNAME=beacsid\) >> %s" % out,
                   "echo         \(ORACLE_HOME = /u01/app/oracle/product/11.2.0/db_1\) >> %s" % out,
                   "echo         \(SID_NAME=beacsid\) >> %s" % out,
                   "echo   \) >> %s" % out,
                   "echo  \) >> %s" % out,
                   "echo >> %s" % out,
                   "echo LISTENER = >> %s" % out,
                   "echo  \(DESCRIPTION_LIST = >> %s" % out,
                   "echo   \(DESCRIPTION = >> %s" % out,
                   "echo    \(ADDRESS = \(PROTOCOL = TCP\)\(HOST = localhost\)\(PORT = 1521\)\) >> %s" % out,
                   "echo   \) >> %s" % out,
                   "echo  \) >> %s" % out,
                   "chown oracle:oinstall %s" % out,
                   "ls -la %s" % out,
                   "cat %s" % out,
                   ]

out = "/u01/app/oracle/product/11.2.0/db_1/network/admin/tnsnames.ora"
ora_tnsnames = [
                "rm %s" % out,     
                "echo ls -la %s" % out,
                "echo  BEACSID = >> %s" % out,
                "echo   \(DESCRIPTION = >> %s" % out,
                "echo    \(ADDRESS = \(PROTOCOL = TCP\)\(HOST = localhost\)\(PORT = 1521\)\) >> %s" % out,
                "echo    \(CONNECT_DATA = >> %s" % out,
                "echo     \(SERVER = DEDICATED\) >> %s" % out,
                "echo     \(SERVICE_NAME = beacsid\) >> %s" % out,
                "echo    \) >> %s" % out,
                "echo   \) >> %s" % out,
                "echo  >> %s" % out,
                "chown oracle:oinstall %s" % out,
                "ls -la %s" % out,
                "cat %s" % out,
                ]

increase_ubuntu_swap =[
                           "sudo dd if=/dev/zero of=/var/swapfile bs=1M count=2048",
                           "sudo chmod 600 /var/swapfile",
                           "sudo mkswap /var/swapfile",
                           "echo /var/swapfile none swap defaults 0 0 | sudo tee -a /etc/fstab",
                           "sudo swapon -a",
                           ]