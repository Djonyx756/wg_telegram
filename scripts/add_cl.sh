#!/bin/bash

var_username=$1

source variables.sh
((vap_ip_local++))

# Запрос имени пользователя
#read -p "Введите имя пользователя: " var_username

wg genkey | tee "/etc/wireguard/${var_username}_privatekey" | wg pubkey | tee "/etc/wireguard/${var_username}_publickey" > /dev/null
echo "[Peer]" >> /etc/wireguard/wg0.conf
echo "PublicKey = $(cat "/etc/wireguard/${var_username}_publickey")" >> /etc/wireguard/wg0.conf
echo "AllowedIPs = 10.10.0.${vap_ip_local}/32" >> /etc/wireguard/wg0.conf
systemctl restart wg-quick@wg0

if [ -f "/etc/wireguard/${var_username}_cl.conf" ]; then
  rm "/etc/wireguard/${var_username}_cl.conf"
fi

echo "[Interface]
PrivateKey = $(cat "/etc/wireguard/${var_username}_privatekey")
Address = 10.10.0.${vap_ip_local}/24
DNS = 8.8.8.8

[Peer]
PublicKey = ${var_public_key}
Endpoint = ${var_ip_global}:51830
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20" | sudo tee -a /etc/wireguard/${var_username}_cl.conf
systemctl restart wg-quick@wg0

# Перезаписываем значение переменной vap_ip_local в файле variables.sh
grep -q "vap_ip_local=" variables.sh && sed -i "s/vap_ip_local=.*/vap_ip_local=${vap_ip_local}/" variables.sh || echo "vap_ip_local=${vap_ip_local}" >> variables.sh

echo "Новый клиент ${var_username} добавлен."

exit 0
