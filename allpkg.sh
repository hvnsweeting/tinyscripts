# get all manual installed pkg
grep 'apt-get install' /var/log/apt/history.log | cut -d' ' -f4- | xargs
#vim git curl ccze i3-wm xclip i3 pidgin ibus-m17n scrot feh irssi

