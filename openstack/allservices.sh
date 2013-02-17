#!/bin/bash

for a in rabbitmq-server libvirt-bin keystone glance-api glance-registry nova-network nova-compute nova-api nova-objectstore nova-scheduler nova-volume nova-consoleauth nova-cert 
do 
    service $a $1;
done

sleep 3 &
nova-manage service list 
