#!/bin/bash

DOMAIN=$1
HOST=$2
if [[ $# -lt "2" ]]; then
	echo "use ./gener DOMAIN HOST"
else
	cat <<- EOF > /etc/nginx/sites-available/$DOMAIN
	server {
		listen      80;
		server_name  $DOMAIN;
		access_log  /var/log/nginx/$DOMAIN.log;
		error_log  /var/log/nginx/$DOMAIN.error.log;
		root   /usr/share/nginx/html;
		index  index.html index.htm;

		location / {
			proxy_pass  http://$HOST;
			proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
			proxy_redirect off;
			proxy_buffering off;
			proxy_set_header        Host            $DOMAIN;
			proxy_set_header        X-Real-IP       \$remote_addr;
			proxy_set_header        X-Forwarded-For \$proxy_add_x_forwarded_for;
		}
	}
	EOF
fi
