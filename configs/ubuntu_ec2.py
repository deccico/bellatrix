"""This configuration holds the list of commands that are going to be applied to a list of ami's. 
This is part of the normal Bellatrix process. The new configuration will be burned in a new ami."""

#list of ami's to process with the below commands
amis = [
       #["ami-8e06f8e7", "Ubuntu10_04_MySQL51_x64"],
       #["ami-f3b6769a", "Ubuntu10_04_DB2_Express-C_9_7_1_x32"],
       #["ami-ba8b72d3", "Ubuntu08.04_MySQL5_0_Postgresql82_x64"],
       #["ami-c48b72ad", "Ubuntu08.04_MySQL5_0_Postgresql83_x64"],
       #[ami-cd69a8a4", "Ubuntu10.04_Postgresql90_x64"]    
       #[ami-cc48b1a5,  "Ubuntu10.04-FF36-MySQL51-x64"]
       ["ami-a7a660ce", "Ubuntu10.04-Postgresql84-x64"]
       ]

#common variables
burn_ami_at_the_end=False   #decide whether or not burning the images at the end
skip_me = False             #decide whether to skip or not this configuration
user = "ubuntu"             #user of the ami's 

#list of commands to execute
import commands

commands = commands.go_home \
            + commands.kill_java_python \
            + commands.clean_home \
            + commands.create_rc_local \
            + commands.deploy_igniter \
            + commands.install_jdk_16_26 \
            + commands.install_jdk_16_27 \
            + commands.install_jdk_17_00 \
            + commands.install_bamboo_assembly \
            + commands.install_s3_cmd       
