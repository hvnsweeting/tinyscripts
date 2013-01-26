#!/bin/bash
set -x
SQL_USER_CREATE=$1
SQL_USERNAME="root"
SQL_PASSWORD="hehehe"

echo "\
drop database if exists $SQL_USER_CREATE;\
create database $SQL_USER_CREATE; \
use $SQL_USER_CREATE;\
grant all on $SQL_USER_CREATE.* to '""$SQL_USER_CREATE""'""@'%' identified by 'hehehe';
" | mysql -u $SQL_USERNAME -p$SQL_PASSWORD 

set +x
