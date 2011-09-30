"""This configuration holds the list of cmds that are going to be applied to a list of ami's. 
This is part of the normal Bellatrix process. The new configuration will be burned in a new ami."""

#list of ami's to process with the below cmds
amis = [
       ["ami-ba8b72d3", "Ubuntu08.04_MySQL5_0_Postgresql82_x64"],
       ["ami-c48b72ad", "Ubuntu08.04_MySQL5_0_Postgresql83_x64"],
       #["ami-8e06f8e7", "Ubuntu10_04_MySQL51_x64"],
       #["ami-cc48b1a5",  "Ubuntu10.04-FF36-MySQL51-x64"],
       #["ami-a7a660ce", "Ubuntu10.04-Postgresql84-x64"],
       #["ami-cd69a8a4", "Ubuntu10.04_Postgresql90_x64"]    
       ]

#common variables
burn_ami_at_the_end=True    #decide whether or not burning the images at the end
skip_me = False             #decide whether to skip or not this configuration
user = "ubuntu"             #user of the ami's 

#list of cmds to execute
import cmds

commands = cmds.kill_java_python \
            + cmds.clean_home \
            + cmds.getCreateRcLocal(user) \
            + cmds.deploy_igniter \
            + cmds.install_jdk_16_26 \
            + cmds.install_jdk_16_27 \
            + cmds.install_jdk_17_00 \
            + cmds.install_bamboo_assembly \
            + cmds.install_s3_cmd       
