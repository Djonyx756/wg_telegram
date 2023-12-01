#!/bin/bash

ip=$1
my_variable=$(grep -n "10.10.0.${ip}" /etc/wireguard/wg0.conf | cut -d ':' -f 1)

sed -i "$(($my_variable-2)),$my_variable d" /etc/wireguard/wg0.conf
systemctl restart wg-quick@wg0
