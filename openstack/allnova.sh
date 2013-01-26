cd /etc/init.d/
for i in $(ls nova-*);do service $i $1; done
