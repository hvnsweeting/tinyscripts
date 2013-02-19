#!/bin/bash
set -x
. rc

SERVICE_NAME=$1
TYPE=$2
PUBLIC_URL="http://192.168.25.66:"
DESCRIPTION="$3"
PUB_PORT_PATH=$4

if [ "$#" != "5" ] ; then  # no specified adminpath
    ADMIN_PORT_PATH=$PUB_PORT_PATH
else
    ADMIN_PORT_PATH="$5"
fi

if [ "$TYPE" = "object-store" ]; then
    #echo "YEAH, it eq"
    PUBLIC_URL="http://127.0.0.1:"
fi

#if [ "$TYPE" = "compute" ]; then
#    PUBLIC_URL="'http://192.168.25.66:"
#    # TODO can't prefix single quote before string
#elif [ "$TYPE" = "volume" ]; then
#    PUBLIC_URL="'http://192.168.25.66:"
#fi

FULL_PUBLIC_URL=$PUBLIC_URL$PUB_PORT_PATH
FULL_ADMIN_URL=$PUBLIC_URL$ADMIN_PORT_PATH


REGION_NAME=RegionOne
SERVICEID=$(keystone --token $TOKEN --endpoint $ENDURL service-create --name=$SERVICE_NAME \
            --type=$TYPE --description="$DESCRIPTION" | grep "id " | cut -d"|" -f3 | tr -d " ")

keystone --token $TOKEN --endpoint $ENDURL endpoint-create --region $REGION_NAME \
            --service_id=$SERVICEID --publicurl=$FULL_PUBLIC_URL --internalurl=$FULL_PUBLIC_URL \
            --adminurl=$FULL_ADMIN_URL

set +x
