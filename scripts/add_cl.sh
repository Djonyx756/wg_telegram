#!/bin/bash

var_username=$1
var_ip_address_glob2="$ip_address_glob"
source variables.sh
((vap_ip_local++))

# Запрос имени пользователя
#read -p "Введите имя пользователя: " var_username

wg genkey | tee "/etc/wireguard/${var_username}_privatekey" | wg pubkey | tee "/etc/wireguard/${var_username}_publickey" > /dev/null
echo "[Peer]" >> /etc/wireguard/wg0.conf
echo "PublicKey = $(cat "/etc/wireguard/${var_username}_publickey")" >> /etc/wireguard/wg0.conf
echo "AllowedIPs = 10.10.0.${vap_ip_local}/32" >> /etc/wireguard/wg0.conf

# Перезапускаем WireGuard интерфейс
wg-quick down wg0
wg-quick up wg0

# Добавим отладочную информацию
ls -la "/etc/wireguard"

if [ -e "/etc/wireguard/${var_username}_cl.conf" ]; then
  rm "/etc/wireguard/${var_username}_cl.conf"
fi

# Добавим отладочную информацию
ls -la "/etc/wireguard"

echo "[Interface]
PrivateKey = $(cat "/etc/wireguard/${var_username}_privatekey")
Address = 10.10.0.${vap_ip_local}/24
DNS = 8.8.8.8

[Peer]
PublicKey = ${var_public_key}
Endpoint = ${ip_address_glob}:51830
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20" | tee -a /etc/wireguard/${var_username}_cl.conf

# Перезапускаем WireGuard интерфейс
wg-quick down wg0
wg-quick up wg0

# Перезаписываем значение переменной vap_ip_local в файле variables.sh
grep -q "vap_ip_local=" variables.sh && sed -i "s/vap_ip_local=.*/vap_ip_local=${vap_ip_local}/" variables.sh || echo "vap_ip_local=${vap_ip_local}" >> variables.sh

echo "ip_address_glob=${ip_address_glob}" >> variables.sh
echo "Новый клиент ${var_username} добавлен."
echo "10.10.0.${vap_ip_local} = ${var_username}" >> cofigs.txt

exit 0

