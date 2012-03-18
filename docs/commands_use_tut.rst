.. _commands_use_tut:

=======================================
An Introduction to Bellatrix commands
=======================================

Bellatrix automates the interaction with EC2 Amazon Web Services. It uses the boto 
library and others. It will wrap the underlying libraries in easy to use utilities 
that are both simple and consistent.

.. contents::


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
--------------------------------------------
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

		The file should contain your 'secret access key' (a string with an approximate length of 50 characters). 
		It is part of your AWS security credentials.
		Please sign into: \nhttps://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key
		in order to get your secret file.

* Private key
	* Location <your_home>/.bellatrix/**ec2.pk**::

		This file is the private key to use in order to connect to your instance. 
		You need to specify before a key-pair in your AWS account. For more details, please refer to:
		http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/generating-a-keypair.html
		The private key file is only used by the 'provision' and 'bewitch' commands. 


Starting an EC2 instance
-----------------------------------------------
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
		* By default you will get t1.micro.
	* Please take a look at: http://aws.amazon.com/ec2/instance-types for more information.
	 
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


Provision an EC2 instance or any host
-----------------------------------------------------
usage: bellatrix provision [-h] [--private_key [PRIVATE_KEY]]
                           configuration user hostname

positional arguments:
  configuration         Python configuration file. E.g. ubuntu.py
  user                  User used to connect to the machine E.g. ubuntu
  hostname              Hostname or simply the ip of the machine.

optional arguments:
  -h, --help            show this help message and exit
  --private_key [PRIVATE_KEY] In case we need to specify a private key to connect to the host. This is empty by default

Saving the state of an instance into a new Amazon AMI
------------------------------------------------------
usage: bellatrix burn [-h] [--wait [WAIT]] instance image_name

positional arguments:
  instance       Instance name. Something like: i-b63c98d4 The instance should be running.
  image_name     Image name. A time stamp will be added to the image name.


Copying files to an S3 bucket
------------------------------------------------------
usage: bellatrix copy2s3 [-h]
                         source bucket [key_prefix]
                         [{private,public-read,public-read-write,authenticated-read}]

positional arguments:
  source                Source file or directory.
  bucket                S3 bucket destination. It must already exist.
  key_prefix            This prefix will be added to the source path we copy. Blank by default. {private,public-read,public-read-write,authenticated-read}
                        ACL policy for the new files in the S3 bucket. If you dont specify anything ACL will be private by default.


Setting launch permissions to an AMI
------------------------------------------------------
usage: bellatrix perm2ami [-h] ami permissions_file

positional arguments:
  ami               AMI name. Something like ami-6ba27502
  permissions_file  Text file with an account number (12 digits number without dashes) on each line.


Stopping an EC2 instance
------------------------------------------------------
usage: bellatrix stop [-h] instance

positional arguments:
  instance    Instance id. Something like i-39e2075d. If you pass "all" then
              all instances will be stopped (unless they are explicitly
              protected)


Terminating an EC2 instance
------------------------------------------------------
usage: bellatrix terminate [-h] instance

positional arguments:
  instance    Instance id. Something like i-39e2075d. If you pass ALL then all
              instances will be terminated (unless they are explicitly
              protected)


Bewitching an AMI or how to start, provision and burn with a single command
--------------------------------------------------------------------------------
usage: bellatrix bewitch [-h] configuration

positional arguments:
  configuration  Python configuration file. E.g. ubuntu.py


