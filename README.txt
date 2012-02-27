===========
Bellatrix
===========

Bellatrix is a comprehensive set of (magic) tools to automate the management of Amazon EC2 services.

    * bellatrix start - Starts a new EC2 instance.
    * bellatrix provision - Applies a set of commands (through SSH) to any host, not only EC2 instances. 
    * bellatrix bewitch - Starts a new instance, applies a configuration to it and finally saves it into a new ami.
    * bellatrix burn - Burns a running instance into a new ami.
    * bellatrix copy2s3 - Copy a file or directory to a S3 bucket.
    * bellatrix perm2ami - Gives permissions to other accounts to launch your ami.
    * bellatrix stop - Stop a given instance or all of them if you use ALL.
    * bellatrix terminate - Terminate a given instance or ALL if you choose so.
    
For more information just execute *bellatrix -h* or *bellatrix command -h*
