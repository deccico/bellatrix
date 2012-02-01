"""
EC2 utilities wrappin boto methods

boto reference in: http://boto.cloudhackers.com/ec2_tut.html

Created on Apr 7, 2011
@author: Adrian Deccico
"""

import datetime
import hashlib
import logging
import os
import sys
import time

import boto
from boto.s3.key import Key

NAME = __file__

class Ec2lib:
    def __init__(self, key, sec):
        self._key = key
        self._sec = sec
        self.ec2 = self.getEC2Connection()
        self.cw = self.getCloudWatchConnection()
        self._running_state = "running"
        self.ERR_CONNECTION_REFUSED = 65280 

    def getCloudWatchConnection(self):
        return boto.connect_cloudwatch(self._key, self._sec)

    def getEC2Connection(self):
        return boto.connect_ec2(self._key, self._sec)

    def getS3Connection(self):
        logging.debug("k:**%s** s:**%s**" % (self._key, self._sec))
        return boto.connect_s3(self._key, self._sec)

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
        name = name.replace(":","-")[:128]
        logging.info("burning instance: %s name: %s, description: %s" % (instance_id, name, description))
        return self.ec2.create_image(instance_id, name, description, no_reboot)

    def getAmiInfo(ami):
        ret = None
        try:
            ret = image = self.getImage(a)
            logging.info("image info: %s" + image)
            
        except:
            logging.error("Error getting information for image:%s " % ami)
        return ret

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
    
    def getDNSName(self, inst, TIME_OUT=300):
        """get DNS name for an instance. This operation could take some time as the startup for new instances is not immediate"""
        logging.info("getting the dns name for instance: " + inst.id + " time out is: " + str(TIME_OUT) + " seconds...")
        step = 3
        while (not inst.dns_name and TIME_OUT > 0):
            TIME_OUT -= step
            inst.update()
            time.sleep(step)
        if not inst.dns_name:
            raise Exception("Sorry, but the instance never returned its address...")
        logging.info("DNS name for %s is %s" % (inst.id, inst.dns_name))
        return inst.dns_name
         
    def waitUntilInstanceIsReady(self, inst, TIME_OUT=300):
        logging.info("waiting until instance: " + inst.id + " is ready. Time out is: " + str(TIME_OUT) + " seconds...")
        step = 3
        #todo: make this concurrent
        while (inst.state !=  self._running_state and TIME_OUT > 0):
            TIME_OUT -= step
            inst.update()
            time.sleep(step)
        if inst.state !=  self._running_state:
            raise Exception("Sorry, but the instance never got the: " + self._running_state + " state")
        logging.info("Instance %s is %s" % (inst.id, inst.state))
        
    def waitForConnectionReady(self, inst, user, key, dns, TIME_OUT=300):
        logging.info("waiting until instance is ready to receive ssh connections. Instance: " + inst.id + " Time out is: " + str(TIME_OUT) + " seconds...")
        tmp_file = "tmp"
        cmd = "ssh -o StrictHostKeyChecking=no -i %s %s@%s '%s' > %s" % (key, user, dns, "echo CONNECTION READY", tmp_file)
        step = 3
        result = self.ERR_CONNECTION_REFUSED
        while (result == self.ERR_CONNECTION_REFUSED and TIME_OUT > 0):
            TIME_OUT -= step
            time.sleep(step)
            logging.info("executing:%s " % cmd )
            result = os.system(cmd)
        if result ==  self._running_state:
            raise Exception("Sorry, but the instance never got ready for SSH connections")
        logging.info("Instance %s is ready for receiving ssh connections. %s" % (inst.id, open(tmp_file).read()))

    def setPermissionsToAmis(self, amis, account_permissions, retry=True):
        """set account permissions to a set of ami's"""
        i=0
        WAIT = 30
        while i < len(amis):
            try:
                image = self.getImage(amis[i])
                if image==None:
                    logging.info("Image doesn't exist in this acount. Finishing execution.")
                    break
                logging.info("image information:%s" % image)
                logging.info("setting execute permissions to %s for accounts:%s" % (amis[i],account_permissions))
                res=image.set_launch_permissions(account_permissions)
                logging.info("operation result:%s " % res )
                i += 1
            except:
                logging.exception("Error setting permissions to ami:%s Please check whether " \
                                  "it exists or your account has proper permissions to access it." % amis[i])
                if retry:
                    logging.info("retrying execution in %s seconds." % WAIT)
                    time.sleep(WAIT)

    def getSecurityGroups(self, groupnames=None):
        """get all security groups from this account"""
        #the following call should return something like:
        #[SecurityGroup:alfresco, SecurityGroup:apache, SecurityGroup:vnc,
        #SecurityGroup:appserver2, SecurityGroup:FTP, SecurityGroup:webserver,
        #SecurityGroup:default, SecurityGroup:test-1228851996]
        #>>> us_group = groups[0]
        #>>> us_group
        #SecurityGroup:alfresco
        #>>> us_group.rules
        #[IPPermissions:tcp(22-22), IPPermissions:tcp(80-80), IPPermissions:tcp(1445-1445)]
        return self.ec2.get_all_security_groups(groupnames)
    
    def authorizeSecurityGroup(self, securityGroup, cidr_ip, from_port, security_group=None, to_port=None, ip_protocol='tcp'):
        to_port = (from_port if to_port == None else to_port)
        logging.info("authorizing... security group:%s, ip_protocol:%s, from_port:%s, to_port:%s cidr:%s sg:%s" % 
                     (securityGroup, ip_protocol, from_port, to_port, cidr_ip, security_group))
        try:
            if cidr_ip != None:
                securityGroup.authorize(ip_protocol=ip_protocol, from_port=from_port, to_port=to_port, cidr_ip=cidr_ip)
            else:
                securityGroup.authorize(ip_protocol=ip_protocol, src_group=security_group, from_port=from_port, to_port=to_port, cidr_ip=cidr_ip)
        except:    
            logging.exception("Exception applying authorization..")
    
    def revokeAllSecurityGroupRules(self, sg):
        logging.info("revoking permissions from security group:%s " % sg)
        for r in sg.rules:
            for g in r.grants:
                #todo detect whether is a security group or an ip
                logging.info("revoking.. sg:%s, ip_protocol:%s, from_port:%s, to_port:%s, cidr:%s" % 
                     (sg, r.ip_protocol, r.from_port, r.to_port, g))
                status = sg.revoke(r.ip_protocol, r.from_port, r.to_port, g)
                logging.info("status: %s" % status)

    def percent_cb(self, complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    def uploadToBucket(self, bucket, file_to_upload, acl="public"):
        bucket = bucket
        k = Key(bucket)
        k.key = file_to_upload
        k.set_acl(acl)
        k.set_contents_from_filename(file_to_upload, cb=self.percent_cb, num_cb=10)
        
    def _copy(self, key_str, path, bucket, acl, pretend, force_copy=False):
        """Perform the actual copy operation.
    
        This method is only called by L{uploadToS3}

        Function originally taken from here:  
        http://www.gordontillman.info/computers/41-web-application-development/88-using-python-boto-library-with-s3
        @param key_str: The string used to lookup the Key within the bucket
        @type key_str: string
        @param path: The path to the local file
        @type path: string
        @param bucket: The bucket we are currently working with
        @type bucket: boto.s3.bucket.Bucket
        @param acl: One of the supported ACL policies
        @type acl: string
        @param pretend: If True, we just log what we would do
        @type pretend: boolean
        @param force_copy: If True, do the copy even if we normally wouldn't
        @type force_copy: boolean
        """
        logging.debug("key_str='%s', path='%s', acl='%s', pretend=%s, "
            "force_copy=%s", key_str, path, acl, pretend, force_copy)
        need_to_copy = True
        key = bucket.get_key(key_str)
        stat = os.stat(path)
        is_dir = os.path.isdir(path)
        if key:
            if is_dir:
                logging.info("'%s' exists - no need to create.", path)
                need_to_copy = False
            elif key.size == stat[6]:
                f = open(path)
                fd = f.read()
                f.close()
                m = hashlib.md5(fd)
                if '"%s"' % m.hexdigest() == key.etag:
                    logging.info("'%s' - no need to copy.  size (%d) "
                    "and md5 (%s) match",
                        path, key.size, key.etag)
                need_to_copy = False
        else:
            key = boto.s3.key.Key(bucket)
            key.key = key_str
        if need_to_copy or force_copy:
            if pretend:
                logging.info("Would copy '%s' to '%s' with ACL '%s'",
                    path, key_str, acl)
            else:
                logging.info("Copying '%s' to '%s' with ACL '%s'",
                    path, key_str, acl)
                key.set_metadata('mode', str(stat[0]))
                key.set_metadata('gid', str(stat[5]))
                key.set_metadata('uid', str(stat[4]))
                key.set_metadata('mtime', str(stat[8]))
                if is_dir:
                    key.set_contents_from_string("",
                        headers={'Content-Type': 'application/x-directory'})
                else:
                    key.set_contents_from_filename(path, cb=self.percent_cb, num_cb=10)
                key.set_acl(acl)
    
    def uploadToS3(self, src, bucket, acl=None, key_prefix="", s3_conn=None,
        filter=None, pretend=None, starting_with=None):
        """Copy the file specified by src (or contained in src if
        it is a directory) to the specified S3 bucket, pre-pending
        the optional key_prefix to the relative path of each
        file within src.

        Function originally taken from here:  
        http://www.gordontillman.info/computers/41-web-application-development/88-using-python-boto-library-with-s3
        @param bucket: The name of the bucket we are working with.  It must
            already exist.
        @type bucket: string
        @param key_prefix: This will be prepended to every source path that
            we copy.  Can be empty.  Often is.
        @type key_prefix: string
        @param src: This is the source file or directory.
        @type src: string
        @param s3_conn: This is an active S3 connection.
        @type s3_conn:  boto.s3.connection.S3Connection
        @param filter: Only files with extensions listed in this filter
            will be candidates for copying.  You can have an empty string
            in this list to copy files with NO file extension.
        @type filter: list of strings
        @param acl: One of the supported ACL policies.
        @type acl: string
        @param pretend: If true, we just log what we would do, but we don't do it.
        @type pretend: boolean
        @param starting_with: An option source file path.  If specified, skips
            all the files preceeding it until this file is reached.
        @type starting_with: string
        @raise boto.exception.S3ResponseError: If you specify
            a non-existing bucket
        """
        if starting_with:
            found_start = False
        else:
            found_start = True
        if not s3_conn:
            s3_conn = self.getS3Connection()
            logging.debug("s3_conn: " + str(s3_conn))
        if not filter:
            filter = ""
        if not acl:
            acl = "public-read"
        if pretend is None:
            pretend = False
        logging.info("bucket=%s, key_prefix=%s, src=%s, filter=%s"
            ", acl=%s, pretend=%s", bucket, key_prefix, src,",".join(filter), acl, pretend)
        logging.debug("bucket list: " + str(s3_conn.get_all_buckets()))
        b = s3_conn.get_bucket(bucket)
        if os.path.isfile(src):
            paths = [('.', [], [src])]
        else:
            paths = os.walk(src)
        for dir in paths:
            dir_key_str = os.path.normpath(
                os.path.join(key_prefix, dir[0])).strip('/')
            dir_path = dir[0]
            if dir_key_str == ".":
                dir_created = True
            else:
                dir_created = False
            for file in dir[2]:
                if not filter or os.path.splitext(file)[1] in filter:
                    path = os.path.normpath(os.path.join(dir[0], file))
                    key_str = os.path.normpath(os.path.join(key_prefix, dir[0],
                        file)).strip('/')
                    if not found_start:
                        if path == starting_with:
                            found_start = True
                        else:
                            continue
                    try:
                        logging.debug("dir_key_str='%s', dir_path='%s', "
                            "key_str='%s', path='%s'", dir_key_str, dir_path,
                            key_str, path)
                        if not dir_created:
                            self._copy(dir_key_str, dir_path, b, acl, pretend)
                            dir_created = True
                        self._copy(key_str, path, b, acl, pretend)
                    except boto.exception.S3ResponseError, e:
                        logging.warn("S3ResponseError '%s' while copying '%s'."
                            "  Will retry 1 time",
                            str(e), path)
                        self._copy(key_str, path, b, acl, pretend, True)


    def getEc2Instance(self, ami, key_name, security_group, instance_type, instance_initiated_shutdown_behavior="terminate"):
        image = self._ec2.getImage(ami)  
        inst = self._ec2.startInstance(image, key_name, security_group, instance_type, self.app_name, instance_initiated_shutdown_behavior="terminate")
        return inst

    def startInstance(self, ami, instance_type, key_name, security_groups):
        inst = self.getEc2Instance(ami, key_name, security_groups.split(), instance_type)
        dns_name = self._ec2.getDNSName(inst)
        self._ec2.waitUntilInstanceIsReady(inst)
        return inst, dns_name
            
