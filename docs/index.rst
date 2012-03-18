.. _index:

=============================================
bellatrix: a set of (magic) AWS EC2 utilities
=============================================

Bellatrix is a set of (magic) command line tools to automate the management of `Amazon Web Services`_.

.. _Amazon Web Services: http://aws.amazon.com/ 
  

Current utilities:

    * bellatrix start - Starts a new EC2 instance. 
    * bellatrix provision - Applies a set of commands (through SSH) to any host, not only EC2 instances. 
    * bellatrix bewitch - Convenient macro-command that starts a new instance, applies a configuration  and finally saves it into a new ami.
    * bellatrix burn - Burns a running instance into a new ami.
    * bellatrix copy2s3 - Copy a file or directory to a S3 bucket.
    * bellatrix perm2ami - Gives permissions to other accounts to launch your ami.
    * bellatrix stop - Stop a given instance or all of them if you use 'all'.
    * bellatrix terminate - Terminate a given instance. Use 'all' to terminate the whole set of instances.
    
For more information just execute *bellatrix -h* or *bellatrix command -h*

.. toctree::
   :maxdepth: 2

   commands_use_tut


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`ref-index`
* :ref:`search`

