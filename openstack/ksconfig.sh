#!/usr/bin/env bash


function runcmd() {
    set -x
    `$1`
    set +x
}

echo -e "You should only run this after installed \033[1m keystone, mysql-server,\
mysql-client, python-mysqldb\033[0m"

echo "Start config KEYSTONE now!"
echo "Remove sqlite database"

# we will use mysql as db
runcmd "rm /var/lib/keystone/keystone.db"

# change bind-address
runcmd "sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf"

runcmd "service mysql restart"
# grant , create db

# config keystone

runcmd "service keystone restart"
runcmd "keystone-manage db_sync"

