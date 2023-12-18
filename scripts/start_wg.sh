#!/bin/bash
source variables.sh
apt update
apt install -y wireguard iptables fish zip unzip iproute2

rm cofigs.txt
touch cofigs.txt
echo "vap_ip_local=1" > variables.sh
ip_address_glob=$(curl -s ifconfig.me)
echo "ip_address_glob=$ip_address_glob" >> variables.sh

internet_interface=$(ip a | awk '/^[0-9]+: .* state UP/ {gsub(/:/,"",$2); print $2}' | grep -E '^ens[0-9]+')
if [ -z "$internet_interface" ]; then
  echo "Интерфейс с доступом в интернет не найден."
  internet_interface="eth0"
fi
ip_address=$(ip a show dev $internet_interface | awk '/inet / {split($2, a, "/"); print a[1]}')
if [ -z "$ip_address" ]; then
  echo "IP-адрес интерфейса $internet_interface не найден."
  exit 1
fi
echo "internet_interface=${internet_interface}" >> variables.sh

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
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o ${internet_interface} -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o ${internet_interface} -j MASQUERADE
" | tee -a /etc/wireguard/wg0.conf

echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# Вместо использования systemctl
wg-quick up wg0

