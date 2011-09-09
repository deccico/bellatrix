ami = "ami-cc48b1a5"
user = "ubuntu"
home = "/home/ubuntu"
skip_me = False

commands = ["cd %s" % home,
            "killall python -w -v",
            "killall java -w -v",
            "rm -rf %s/*" % home,
            "echo \#\!/bin/sh -e > rc.local",
            "echo ulimit -n 8192 >> rc.local",
            "echo cd %s >> rc.local" % home,
            "echo su -c /home/ubuntu/igniter.py - ubuntu >> rc.local",
            "sudo rm /etc/rc.local",
            "chmod a+x rc.local",
            "sudo cp rc.local /etc/rc.local",
            "cat /etc/rc.local",
            "wget https://s3.amazonaws.com/bamboo-igniter/igniter.py",
            "sed -i s/beac_agent/cbac_agent/ igniter.py",
            "chmod a+x igniter.py"
            ]
