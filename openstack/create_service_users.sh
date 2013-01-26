#!/bin/bash
# usage: ./create_service_users.sh username

ENDURL=http://192.168.25.66:35357/v2.0
TOKEN=ADMINTOKEN
SERVICE_TENANT_ID=aaa75a4fb10c46a0ad83f6f2b702d1b3
ADMINROLE=b398100f629c4a44974297444a71c23b

userid=$(keystone --token $TOKEN --endpoint $ENDURL \
        user-create --tenant_id $SERVICE_TENANT_ID --name $1 --pass $1 \
        | grep id $addout | cut -d'|' -f3- | tr -d " " | tr -d "|")

keystone --token $TOKEN --endpoint $ENDURL  user-role-add --user $userid --tenant_id $SERVICE_TENANT_ID --role $ADMINROLE
