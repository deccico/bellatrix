ami = [
       #["ami-5918db30", "Ubuntu10_04_FF36_MySQL51_x64"]
       #["ami-8e06f8e7", "Ubuntu10_04_MySQL51_x64"],
       #["ami-f3b6769a", "Ubuntu10_04_DB2_Express-C_9_7_1_x32"],
       #["ami-ba8b72d3", "Ubuntu08.04_MySQL5_0_Postgresql82_x64"],
       #["ami-c48b72ad", "Ubuntu08.04_MySQL5_0_Postgresql83_x64"],
       #["ami-a7a660ce", "Ubuntu10.04_Postgresql84_x64"],
       #[ami-cd69a8a4", "Ubuntu10.04_Postgresql90_x64"]    
       ]
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
