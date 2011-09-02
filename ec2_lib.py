"""
EC2 utilities wrappin boto methods

boto reference in: http://boto.cloudhackers.com/ec2_tut.html

Created on Apr 7, 2011
@author: Adrian Deccico
"""

import boto
import datetime
import logging
import os

NAME = __file__

class Ec2lib:
    def __init__(self, key, sec):
        self.VERSION = "20110826"
        self._key = key
        self._sec = sec
        self.ec2 = self.getEC2Connection()
        self.cw = self.getCloudWatchConnection()
        logging.info("%s - %s" % (NAME, self.VERSION))

    def getCloudWatchConnection(self):
        return boto.connect_cloudwatch(self._key, self._sec)

    def getEC2Connection(self):
        return boto.connect_ec2(self._key, self._sec)

    def getCPUMetric(self, instance_name):
        hours_span = self.hours
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(hours=hours_span)
        return self.cw.get_metric_statistics(self.PERIOD, start, end, self.metric,
                                          self.NAMESPACE, self.function,
                                          instance_name)

    def getReservations(self):
        return self.ec2.get_all_instances()

    def getImage(self, ami):
        return self.ec2.get_image(ami)

    def createImage(self, instance_id, name, description=None, no_reboot=False):
        """
        Will create an AMI from the instance in the running or stopped
        state. 
        
        :type instance_id: string
        :param instance_id: the ID of the instance to image.

        :type name: string
        :param name: The name of the new image

        :type description: string
        :param description: An optional human-readable string describing
                            the contents and purpose of the AMI.

        :type no_reboot: bool
        :param no_reboot: An optional flag indicating that the bundling process
                          should not attempt to shutdown the instance before
                          bundling.  If this flag is True, the responsibility
                          of maintaining file system integrity is left to the
                          owner of the instance.
        
        :rtype: string
        :return: The new image id
        """        
        return self.ec2.createImage(instance_id, name, description, no_reboot)

    def startInstance(self, image, key_name, security_group, instance_type, owner_name=os.path.basename(__file__), instance_initiated_shutdown_behavior="terminate"):
        """
        starts an instance given an 'image' object
        
        :instance_initiated_shutdown_behavior: string. Valid values are stop | terminate
        
        :instance_type: string
        :param instance_type: The type of instance to run.  Current choices are:
                          m1.small | m1.large | m1.xlarge | c1.medium |
                          c1.xlarge | m2.xlarge | m2.2xlarge |
                          m2.4xlarge | cc1.4xlarge
        :owner_name: string. Just the entity that initiated the instance. You will see the name in the 'tag name'. This library by default.

        """
        logging.info("starting image: " + image.id)
        #img.run(key_name='cloudright', security_groups=['test1'], instance_type='m1.large')
        reservation = image.run(1, 1, 
                      key_name, security_group, 
                      instance_type=instance_type, 
                      instance_initiated_shutdown_behavior=instance_initiated_shutdown_behavior)
        logging.info("we got %d instance (should be only one)." % len(reservation.instances))
        i = reservation.instances[0]
        i.update()
        logging.info("instance %s is now: %s" % (i.id, i.state))
        self.tagInstance(i.id, "Name",  owner_name + " started me")
        return i

    def stopInstance(self, i):
        i.stop()
    
    def tagInstance(self, instance, key, value):
        logging.info("tagging instance:%s key:%s value:%s" % (instance, key, value))
        self.ec2.create_tags([instance], {key: value})
    
    def terminateInstance(self, i):
        i.terminate()        

    def getInstances(self):
        instances = []
        dict_inst = {}
        for img in self.getReservations():
            for r in img.instances:
                if self.RUNNING == r.state_code:
                    i = str(r).split(":")[1]
                    #skip ami's and instances
                    if r.image_id in self._exceptions or i in self._exceptions:
                        logging.info("skipping %s as it is in the exception list" % str(r))
                        continue
                    instances.append([{"InstanceId":i}, r])
        return instances


    def destroyIdleInstances(self):
        logging.info("Killing running instances consistently under the %s%s cpu threshold that" \
        " have run for at least %s hour/s" % (self.threshold, "%", self.hours))
        instances = self.getInstances()
        logging.info("getting active instances...")
        for i in instances:
            try:
                instance_name = i[0]
                instance = i[1]
                metrics = self.getCPUMetric(instance_name)
                logging.info("getting metrics for instance: %s" % (str(instance_name)))
                kill_it = True
                for mt in metrics:
                        val = mt[u'Maximum']
                        if val > self.threshold:
                            kill_it = False
                        logging.info("CPU use: %s" % (str(val) + "%"))
                if kill_it:
                    if len(metrics) >= self.expected_samples:
                        logging.info("killing %s... AWS ident:XXX%s" % (instance_name, self._key[len(self._key) - 3:]))
                        if not self.dryrun:
                            instance.stop()
                        else:
                            logging.info("Dry run mode, I am not feeling like killing anyone..." % instance_name)
                    else:
                        logging.info("This instance was not running enough time. Forgiving %s..." % instance_name)
                        logging.info("Len metrics:%s expected samples:%s" % (len(metrics), self.expected_samples))
            except:
                logging.exception("Error: ")

    def setExceptions(self, elements):
        """AMI's and instances put into this list will 
        be skipped in the shutdown process"""
        for e in elements:
            if e not in self.exceptions:
                self.exceptions.append(e)
        



