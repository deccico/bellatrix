.. _commands_use_tut:

=======================================
An Introduction to Bellatrix commands
=======================================

Bellatrix automates the interaction with EC2 Amazon Web Services. It uses the boto 
library and others. Bellatrix wraps the underlying libraries in easy to use utilities 
that are both simple and consistent.


Installing Bellatrix
--------------------
If you already have pip, just execute::

	pip install bellatrix

Other option is to go to: http://pypi.python.org/pypi/bellatrix/ 
download the .tar.gz package and then::

	tar xvzf bellatrix-[version].tar.gz
	cd belatrix-[version]
	python setup.py   #this will require admin access
	

Setting your AWS credentials
---------------------
Bellatrix only needs three single files in order to help you access to your AWS EC2 
resources. Not all the tools need all the files. If they are not present Bellatrix 
will show a nice message explaining what file (and where) you need to provide.

* Access key id
	* Location <your_home>/.bellatrix/**key**::
	
		Your 'access key id' will be something like AKIAIU**************) and is part of your AWS security credentials. 
		If you don't remember it please sign into: 
		https://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key

* Secret file
	* Location <your_home>/.bellatrix/**secret**::

		The file should contain your 'secret access key' (a string with an approximate length of 50 characters) and is part of your AWS security credentials.
		Please sign into: \nhttps://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key
		in order to get your secret file.

* Private key
	* Location <your_home>/.bellatrix/**ec2.pk**::

		This file is the private key to use in order to connect to your instance. 
		You need to specify before a key-pair in your AWS account. For more details, please refer to:
		http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/generating-a-keypair.html
		The private key file is only used by the 'provision' and 'bewitch' commands. 


Starting an EC2 instance
========================
In order to start an instance, just type::
	
	bellatrix start ami key_name 

The complete usage, with optional parameters is::

	bellatrix start ami key_name [--security_groups [SECURITY_GROUPS]] [--type [type]] [--new_size [NEW_SIZE]]

-------------------

**Parameters list**

* ami - Amazon Machine Image. A pre-configured operating system with its applications. 
	* The code will be something like ami-6ba27502. You can access a large set of AMI's in:
		* https://aws.amazon.com/amis
		* http://cloud.ubuntu.com/ami/	
		* http://thecloudmarket.com/ 
	* Or you can easily generate your own AMI using Bellatrix's commands.

* key_name - Name of the ssh key-pair name that will be applied to your instance. 
	* The key name is the name of the two files (public and private keys) that you can use to connect to your EC2 instance.
	* AWS will put the public file in the instance while you need to use the private one to connect to your instance::

		ssh -i private_key user@public_dns
	* In order to generate your 'key name', please refer to: http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/generating-a-keypair.html
	* If you are starting a Windows AMI then you would normally use RDP instead of this ssh key. 
	
* [optional] security_groups [SECURITY_GROUPS]
	* Comma separated list (with no spaces) of the security groups that will be applied to the new instance. 
	* It can be only one. By default it will be "default"
	
* [optional] type.
	* Instance type. The same AMI can be launched with different 'hardware' options.
	* You can choose between:
		* m1.small,m1.medium,m1.large,m1.xlarge,t1.micro,m2.xlarge,m2.2xlarge,m2.4xlarge,c1.medium,c1.xlarge,cc1.4xlarge,cc2.8xlarge
		By default you will get t1.micro.
	Please take a look at: http://aws.amazon.com/ec2/instance-types for more information.
	 
* [optional] new_size [NEW_SIZE] (in giga bytes).
	* An EBS AMI can be started with a larger size just by using this option. If you then save the instance into a new AMI then this will be the default value.
	* If the file system is ext4, then you are done. If not, you will need to execute one of this commands:: 

		# ext3 root file system (most common)
		sudo resize2fs /dev/sda1
		#(OR)
		sudo resize2fs /dev/xvda1
		
		# XFS root file system (less common):
		sudo apt-get update && sudo apt-get install -y xfsprogs
		sudo xfs_growfs /
		
		# In the case of Windows, you can use the graphical administration tools.                        


