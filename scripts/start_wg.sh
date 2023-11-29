#!/bin/bash
source variables.sh
apt update
apt install -y wireguard iptables fish
wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
chmod 600 /etc/wireguard/privatekey
var_private_key=$(cat /etc/wireguard/privatekey)
var_public_key=$(cat /etc/wireguard/publickey)
echo "var_private_key=\"$var_private_key\"" >> variables.sh
echo "var_public_key=\"$var_public_key\"" >> variables.sh
echo "[Interface]
PrivateKey = ${var_private_key}
Address = 10.10.0.1/24
ListenPort = 51830
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
 " | sudo tee -a /etc/wireguard/wg0.conf
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
systemctl enable wg-quick@wg0.service
systemctl start wg-quick@wg0.service
