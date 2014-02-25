#!/bin/bash

set +x
for i in libass-dev libgpac-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libx11-dev libxext-dev libxfixes-dev pkg-config texi2html zlib1g-dev; do
    apt-cache show $i | egrep -v `apt-cache show iproute | cut -d':' -f1 | grep -v Descrip | grep -v '^ ' | egrep -v 'Package|Installed-Size|Depends|Provides' | sed -e 's/^I //' -e '/^$/d' -e 's/$/:/' | tr '\n' '|' | sed 's/|$//g'`
    echo
done
