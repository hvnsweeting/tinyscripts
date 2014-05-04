#! /bin/bash
# Use: ./salt-minion-installer.sh salt.master.address
# Example: ./salt-minion-installer.sh 123.23.23.23
# lamdt

add-apt-repository -y ppa:saltstack/salt

apt-get update

echo "$1 salt" >> /etc/hosts

apt-get -y install python-software-properties salt-minion
