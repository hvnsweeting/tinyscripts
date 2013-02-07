#!/bin/bash

for host in '192.168.122.30' '192.168.122.250';do
    ssh-copy-id $host
done

