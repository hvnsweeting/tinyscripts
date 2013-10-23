#!/bin/bash
# by HVN <hvnsweeting@gmail.com>
# at Wed Oct 23 15:22:52 ICT 2013

repo_link="http://nginx.org/packages/ubuntu/pool/nginx/n/nginx/"
data_dir=/home/hvn/.usr/local/nginx
/bin/mkdir -p "$data_dir"
pwd_=$(/bin/pwd)
cd "$data_dir"
/usr/bin/wget -O today $repo_link
echo "Checked at `date`" >> log

if [ ! -e last ]; then
    /bin/cp today last
else
    if [ `diff today last -q | wc -l` -eq 0 ]; then
        /usr/bin/diff today last >> log
        /bin/rm last
        /bin/cp today last
    fi
fi
cd $pwd_
