""" common utilities, meant to be used as build blocks by configs. 

Please, keep every block independent from the others. 
"""

#special cases are not special enough... PEP20
skip_me = True
amis = []
user = ""

def removeSudo(cmds):
    list = cmds
    for i in range(len(list)):
        list[i] = list[i].replace("sudo ", "")
    return list
    

upgrade_ubuntu = ["sudo apt-get update -y",
                  "sudo apt-get upgrade -y",
                  ]

kill_java_python = ["killall python -w -v",
                    "killall java -w -v",
                    ]

clean_home = ["rm -rf $HOME/*"]

def getCreateRcLocal(user):
    rc_local = "$HOME/rc.local"
    create_rc_local = ["echo \#\!/bin/sh -e > %s" % rc_local,
                       "echo ulimit -n 8192 >> %s" % rc_local,
                       "echo cd $HOME >> %s" % rc_local,
                       "echo su -c $HOME/igniter.py - %s >> %s" % (user, rc_local),
                       "sudo rm /etc/rc.local",
                       "chmod a+x %s" % rc_local,
                       "sudo cp rc.local /etc/rc.local",
                       "cat /etc/rc.local",
                       ]
    return create_rc_local

deploy_igniter = ["wget https://s3.amazonaws.com/bamboo-ec2-igniter/igniter.py",
                  "chmod a+x igniter.py"
                  ]

upgrade_ubuntu_distro = ["sudo apt-get update -y",
                         "sudo apt-get upgrade -y"
                         ]

jdk = "jdk-6u26-linux-x64.bin"
install_jdk_16_26 = [
                     "wget https://s3.amazonaws.com/bamboo-ec2/%s" % jdk,
                     "chmod a+x %s" % jdk,
                     "echo |./%s >out_jdk 2>&1" % jdk,
                     "cat out_jdk",
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv jdk1.6.0_26 /opt/java/sdk/",
                     ]

jdk = "jdk-6u27-linux-x64.bin"
install_jdk_16_27 = [
                     "wget https://s3.amazonaws.com/bamboo-ec2/%s" % jdk,
                     "chmod a+x %s" % jdk,
                     "echo |./%s >out_jdk 2>&1" % jdk,
                     "cat out_jdk",
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv jdk1.6.0_27 /opt/java/sdk/",
                     ]

jdk = "jdk-7-linux-x64.tar.gz"
install_jdk_17_00  = [
                     "wget https://s3.amazonaws.com/bamboo-ec2/%s" % jdk,
                     "tar -xvzf %s" % jdk,
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv jdk1.7.0 /opt/java/sdk/",
                     ]

install_bamboo_assembly =[
                           "wget https://s3.amazonaws.com/bamboo-ec2-jbac/jbac_agent.zip",
                           "unzip -o jbac_agent.zip",
                           "cp bamboo-elastic-agent/bin/bamboo-ec2-metadata $HOME/bamboo-ec2-metadata.exe"
                           ]

out = "$HOME/.s3cfg"
install_s3_cmd = [
                  "wget https://s3.amazonaws.com/bamboo-ec2/s3cmd.zip",
                  "unzip -o -d $HOME/s3cmd s3cmd.zip",
                  "cd $HOME/s3cmd/s3cmd;sudo python setup.py install",
                  "echo [default] > %s" % out,
                  "echo access_key = AKIAJ55SDWUCH2HHBUCA >> %s" % out,
                  "echo secret_key = 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 >> %s" % out,
                  ]

