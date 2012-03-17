===========
Bellatrix
===========

Bellatrix is a set of (magic) tools to automate the use of Amazon EC2 services.

[Online documentation](http://bellatrix.readthedocs.org/) 

Quick reference:

    * bellatrix start - Starts a new EC2 instance.
    * bellatrix provision - Apply a set of commands (through SSH) to any host, not only EC2 instances. 
    * bellatrix bewitch - Start a new instance, applies a configuration to it and finally saves it into a new ami.
    * bellatrix burn - Burn a running instance into a new ami.
    * bellatrix copy2s3 - Copy a file or directory to a S3 bucket.
    * bellatrix perm2ami - Give permissions to other accounts to launch your ami.
    * bellatrix stop - Stop a given instance or all of them if you pass the "all" argument. Stopping an instance will shut-down the instance but preserve data on the EBS volume.
    * bellatrix terminate - Terminate a given instance or all of them if you pass the "all" parameter. Terminating an instance will shut it down and delete data on the EBS volume.
    
For more information just execute *bellatrix -h* or *bellatrix command -h*
