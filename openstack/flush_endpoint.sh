#!/bin/bash

# delete all endpoints
. rc

IDS=$(keystone --token $TOKEN --endpoint $ENDURL endpoint-list | cut -d"|" -f2 | tail -n+4 | head -n-1 | xargs)
for id in $IDS; do
    keystone --token $TOKEN --endpoint $ENDURL endpoint-delete $id
done
