#!/bin/sh
# Script help create a virtualenv for running newest version of Salt
#TODO install all dependencies
#for now, just install newest salt from ppa then ``apt-get purge -y salt-*``

#if [ $EUID -ne 0 ]; then
#    echo "This script must run by root"
#fi
if [ -z $1 ]; then
    echo "USAGE: $0 path_to_create_devsalt_env"
    exit 1
fi

dest_dir=$1
if [ -e $dest_dir ]; then
    echo `pwd`/"$dest_dir is already existed, remove it"
    exit 1
fi

if [ `which virtualenv2` ]; then
    venv_cmd=virtualenv2
else
    venv_cmd=virtualenv
fi

code_only=$1
$venv_cmd --system-site-packages $dest_dir
. $dest_dir/bin/activate

cd $dest_dir

if [ -z $code_only ]; then
    git clone git://github.com/saltstack/salt.git mainstream
    pip install -e mainstream
else
    python2 -c 'import urllib; urllib.urlretrieve("https://github.com/saltstack/salt/archive/develop.tar.gz", "develop.tar.gz")'
    tar xzf develop.tar.gz
    pip install -e salt-develop
fi

if ( ! grep _SALTDEVENV_ ~/README 2>&1 > /dev/null ); then
    echo "_SALTDEVENV_ installed at $(date), use ``source $dest_dir/bin/activate`` to active venv for dev SaltStack``" >> ~/README
fi
echo "Use ``source $dest_dir/bin/activate`` to active venv for dev SaltStack``"

