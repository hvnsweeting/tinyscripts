#!/bin/bash

DBNAME=nova
USERNAME=nova
PASSWD=openstack

mysql -u root -phehehe -Be "create database $DBNAME";
mysql -u root -phehehe -Be "grant all on $DBNAME.* to $USERNAME@'%' identified by '$PASSWD'";
mysql -u root -phehehe -Be "grant all on $DBNAME.* to $USERNAME@'localhost' identified by '$PASSWD'";
