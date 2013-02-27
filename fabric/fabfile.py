from fabric.api import *

SALT_MASTER = '192.168.122.1'
GUEST_NAME = "ubun2"

def myhost():
    env.hosts = ["192.168.122.88"]

def master():
    env.hosts = [SALT_MASTER]

def copyssh():
    for host in env.hosts:
        local("ssh-copy-id " + host)

def change_hostname():
    hostname = GUEST_NAME
    sudo("echo %s > /etc/hostname" % hostname)
    sudo("sed -i 's/127.0.1.1.*/127.0.1.1\t%s/' /etc/hosts" % hostname)

def salt_bootstrap():
    sudo('wget -O - http://bootstrap.saltstack.org | sudo sh')

def salt_config():
    sudo("sed -i 's/[#]*master:.*/master: %s/g' /etc/salt/minion" % SALT_MASTER)
    sudo('service salt-minion restart')
