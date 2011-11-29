"""This configuration holds the list of cmds that are going to be applied to a list of ami's. 
This is part of the normal Bellatrix process. The new configuration will be burned in a new ami."""

#list of ami's to process with the below cmds
amis = [
       ["ami-f3b6769a", "Ubuntu10_04_DB2_Express-C_9_7_1_x32"],
       ]

#common variables
burn_ami_at_the_end=True    #decide whether or not burning the images at the end
skip_me = False             #decide whether to skip or not this configuration
user = "ubuntu"              #user of the ami's 

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
            + cmds.install_s3_cmd \
            + cmds.increase_ubuntu_swap       

