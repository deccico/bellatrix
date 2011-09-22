""" common utilities, meant to be used as build blocks by configs. 

Please, keep every block independent from the others. 
"""

#special cases are not special enough...
skip_me = True
amis = []
user = ""

go_home = ["cd $HOME"]

upgrade_ubuntu = ["sudo apt-get update -y",
                  "sudo apt-get upgrade -y",
                  ]

kill_java_python = ["killall python -w -v",
                    "killall java -w -v",
                    ]

clean_home = ["rm -rf $HOME/*"]

create_rc_local = ["echo \#\!/bin/sh -e > rc.local",
                   "echo ulimit -n 8192 >> rc.local",
                   "echo cd $HOME >> rc.local",
                   "echo su -c $HOME/igniter.py - ubuntu >> rc.local",
                   "sudo rm /etc/rc.local",
                   "chmod a+x rc.local",
                   "sudo cp rc.local /etc/rc.local",
                   "cat /etc/rc.local",
                   ]

deploy_igniter = ["wget https://s3.amazonaws.com/bamboo-igniter/igniter.py",
                  "sed -i s/beac_agent/cbac_agent/ igniter.py",
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
                     "echo |./%s >out_jdk 2>&1" % jdk,
                     "cat out_jdk",
                     "sudo mkdir -p /opt/java/sdk/",
                     "sudo mv jdk1.7.0 /opt/java/sdk/",
                     ]

install_bamboo_assembly = [
                           "wget https://s3.amazonaws.com/bamboo-ec2-jbac/jbac_agent.zip",
                           "unzip -o -d $HOME/bamboo-elastic-agent jbac_agent.zip"
                           ]

install_s3_cmd = [
                  "wget https://s3.amazonaws.com/bamboo-ec2/s3cmd.zip",
                  "unzip -o -d $HOME/s3cmd s3cmd.zip"
                  ] 

