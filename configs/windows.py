"""This configuration holds the list of cmds that are going to be applied to a list of ami's. 
This is part of the normal Bellatrix process. The new configuration will be burned in a new ami."""

#list of ami's to process with the below cmds
amis = [
       ["ami-7ce61b15", "Windows-2008-IE8-x64"],
       ["ami-dc8870b5", "Win2008-IE9-FF4-CHR-SF-x64"],
       ["ami-8248b1eb", "Windows-2008-Active-Directory-x64"],
       ]

#common variables
burn_ami_at_the_end=False    #decide whether or not burning the images at the end
skip_me = True               #decide whether to skip or not this configuration
user = "Administrator"       #user of the ami's 

#list of cmds to execute
import cmds

commands = []



