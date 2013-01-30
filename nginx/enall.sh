#!/bin/bash

avai="/etc/nginx/sites-available"
set -x
for i in $avai/*; do
	echo $i
	filename=`basename $i`
	ln -s $i /etc/nginx/sites-enabled/$filename
done
set +x
