set -x
sed -i 's_sqlite.*_mysql://nova:openstack@127.0.0.1/nova_' /etc/nova/nova.conf
set +x
