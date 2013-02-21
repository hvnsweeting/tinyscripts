from fabric.api import *

SALT_MASTER = '192.168.122.1'
ADMIN = '192.168.122.30'
OSD = '192.168.122.250'
CLIENT = '192.168.122.213'
def master():
    env.hosts = [ADMIN]

def server():
    env.hosts = [OSD]

def client():
    env.hosts = [CLIENT]

def change_hostname():
    hostname = "ubun2"
    sudo("echo %s > /etc/hostname" % hostname)
    sudo("sed -i 's/127.0.1.1.*/127.0.1.1\t%s/' /etc/hosts" % hostname)

def salt_bootstrap():
    sudo('wget -O - http://bootstrap.saltstack.org | sudo sh')

def salt_config():
    sudo("sed -i 's/[#]*master:.*/master: %s/g' /etc/salt/minion" % SALT_MASTER)
    sudo('service salt-minion restart')
