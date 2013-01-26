#!/usr/bin/env bash
#USAGE: ./upload_disk.sh ttylinux ttylinux-uec-amd64-12.1_2.6.35-22_1-vmlinuz ttylinux-uec-amd64-12.1_2.6.35-22_1-initrd ttylinux-uec-amd64-12.1_2.6.35-22_1.img 
#run ./upload_disk.sh DISTRONAME kernelFILE ramdiskFILE mainFILE
#You should export neccesary var before run this
#export OS_TENANT_NAME="openstackDemo"
#export OS_USERNAME="adminUser"
#export OS_PASSWORD="secretword"
#export OS_AUTH_URL="http://localhost:5000/v2.0/"

DISKNAME=$1 #tty-linux
KERNEL=$2
RAMDISK=$3
MAINDISK=$4

set -x

dformat="aki"
DISKTYPE="-kernel"
kernelret=$(glance add name=$DISKNAME$DISKTYPE disk_format=$dformat container_format=$dformat < $KERNEL)
kernel_id=$(echo $kernelret | sed -n 's/.*ID: //p')

dformat="ari"
DISKTYPE="-ramdisk"
ramret=$(glance add name=$DISKNAME$DISKTYPE disk_format=$dformat container_format=$dformat < $RAMDISK)
ramdisk_id=$(echo $ramret | sed -n 's/.*ID: //p')

dformat="ami"
DISKTYPE=''
EXTRA="kernel_id=$kernel_id ramdisk_id=$ramdisk_id "
glance add name=$DISKNAME$DISKTYPE disk_format=$dformat container_format=$dformat $EXTRA < $MAINDISK

glance index
set +x
