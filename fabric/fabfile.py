from fabric.api import *


def server():
    env.hosts = ['192.168.122.30']

def client():
    env.hosts = ['192.168.122.250']


def change_hostname():
    hostname = "ubun2"
    sudo("echo %s > /etc/hostname" % hostname)
    sudo("sed -i 's/127.0.1.1.*/127.0.1.1\t%s/' /etc/hosts" % hostname)

def install_ceph():
    run('wget -q -O- https://raw.github.com/ceph/ceph/master/keys/release.asc | sudo apt-key add -')
    run('echo deb http://ceph.com/debian/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list')
    sudo('apt-get update && sudo apt-get install ceph')

def copy_ceph_conf():
    for host in env.hosts:
        local('scp ceph.conf %s:/home/hvn/' % host)

def create_dirs():
    sudo('mkdir -p /var/lib/ceph/osd/ceph-0')
    sudo('mkdir -p /var/lib/ceph/osd/ceph-1')
    sudo('mkdir -p /var/lib/ceph/mon/ceph-a')
    sudo('mkdir -p /var/lib/ceph/mds/ceph-a')

def mkcephfs():
    run('cd /etc/ceph')
    sudo('mkcephfs -a -c /etc/ceph/ceph.conf -k ceph.keyring')

def rbd():
    #run("rbd create foo --size 2048")
    #run('sudo modprobe rbd')
    #sudo("rbd map foo --pool rbd --name client.admin")
    #sudo("mkfs.ext4 -m0 /dev/rbd/rbd/foo")
    #sudo("mkdir /mnt/myrbd")
    #sudo("mount /dev/rbd/rbd/foo /mnt/myrbd")
    pass
