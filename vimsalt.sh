#!/bin/bash

# saltvimplus
# ===========
#
# A simple vim setup ready for writing saltstack.org states
#
# This vim setup support:
#
# - yaml.vim : vim plugin that helps highlight YAML syntax, jinja files
#
# - Snippet.vim: supports snippets for quickly write new state.
#
# - A simple vimrc

echo "This install script requires: vim git"
#apt-get install -y vim git

if ( ! grep _VIMSALT_ ~/README |& >/dev/null); then
    echo "_VIMSALT_ installed, vim now supports .SLS and snippet" >> ~/README
fi

tempdir=$(mktemp -d)
cd $tempdir
git clone git://github.com/saltstack/salt-vim.git
git clone git://github.com/hvnsweeting/snipmate.vim.git

if [ -d ~/.vim ]; then
    backup_dir=/tmp/dotvim_`date +%Y%m%d_%H%M%S`
    echo "BACKUP old ~/.vim to $backup_dir"
    mv ~/.vim $backup_dir
fi

mkdir ~/.vim

for dir in *; do
    cp -r $dir/* ~/.vim
done

python2 -c 'import urllib, os; urllib.urlretrieve("https://raw.github.com/hvnsweeting/hvnrc/master/vimrc", os.path.expanduser("~/.vimrc"))'
rm -rf $tempdir
