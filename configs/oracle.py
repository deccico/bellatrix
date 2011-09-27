"""This configuration holds the list of cmds that are going to be applied to a list of ami's. 
This is part of the normal Bellatrix process. The new configuration will be burned in a new ami."""

#list of ami's to process with the below cmds
amis = [
       ["ami-1659a77f", "Oracle_11_2_x64"],
       ]

#common variables
burn_ami_at_the_end=True    #decide whether or not burning the images at the end
skip_me = False             #decide whether to skip or not this configuration
user = "root"             #user of the ami's 

#list of cmds to execute
import cmds

commands = cmds.kill_java_python \
            + cmds.clean_home \
            + cmds.getCreateRcLocal("oracle") \
            + cmds.deploy_igniter \
            + cmds.install_jdk_16_26 \
            + cmds.install_jdk_16_27 \
            + cmds.install_jdk_17_00 \
            + cmds.install_bamboo_assembly \
            + cmds.install_s3_cmd       

commands = cmds.removeSudo(commands)


#old /etc/rc.local
#$ cat /etc/rc.local 
##!/bin/sh
##
## This script will be executed *after* all the other init scripts.
## You can put your own initialization stuff in here if you don't
## want to do the full Sys V style init stuff.
#
#touch /var/lock/subsys/local
#
### Begin EC2 SETUP ##
#
## Update the Amazon EC2 AMI creation tools
#echo " + Updating ec2-ami-tools"
#wget http://s3.amazonaws.com/ec2-downloads/ec2-ami-tools.noarch.rpm && \
#rpm -Uvh ec2-ami-tools.noarch.rpm && \
#echo " + Updated ec2-ami-tools"
#
## Update the Amazon EC2 API tools
#echo " + Updating ec2-api-tools"
#wget http://s3.amazonaws.com/ec2-downloads/ec2-api-tools.zip && \
#unzip -o ec2-api-tools.zip
#rpm -Uvh ec2-ami-tools.noarch.rpm && \
#echo " + Updated ec2-ami-tools"
#
## Randomize root and oracle password
#if [ -f "/root/firstrun" ] ; then
#  dd if=/dev/urandom count=50|md5sum|passwd --stdin root
#  dd if=/dev/urandom count=50|md5sum|passwd --stdin oracle
#  rm -f /root/firstrun
#else
#  echo "* Firstrun *" && touch /root/firstrun
#fi
#
### End EC2 SETUP
#
##starting bamboo agent
#cd /home/oracle/
#su -c /home/oracle/run_bambooner_run.py  - oracle
