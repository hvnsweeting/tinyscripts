#!/bin/bash

REALDIR=$(cd $1 && pwd)
HYPHENS="-----"

cd "$REALDIR"
ABSENTSLS=0
for f in *; do
	if [[ "$f" == *".jinja2" ]]; then
		grep -q "message_do_not_modify" "$f" || echo "$HYPHENS $f NOT CONTAIN HEADER $HYPHENS"
	elif [[ "$f" == *".sls" ]]; then
		echo "$f"
		if [[ "$f" == "absent.sls" ]]; then
			ABSENTSLS=1
		fi
	else
		echo "$HYPHENS $f EXTENSION IS BAD $HYPHENS"
	fi
done

if [[ ABSENTSLS -eq 0 ]]; then
	echo "$HYPHENS LACKING OF ABSENT.SLS $HYPHENS"
fi
