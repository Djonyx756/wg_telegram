#!/bin/bash

ip_address=$1
ip_address=10.10.0.$ip_address
file_path="cofigs.txt"

# Проверяем, передан ли IP-адрес в качестве аргумента
if [ -z "$ip_address" ]; then
  echo "Не указан IP-адрес."
  exit 1
fi

# Проверяем, существует ли файл
if [ ! -f "$file_path" ]; then
  echo "Файл $file_path не существует."
  exit 1
fi

# Считываем имя пользователя из файла
username=$(awk -F" = " -v ip="$ip_address" '$1 == ip {print $2}' "$file_path")

if [ -z "$username" ]; then
  echo "Пользователь с IP-адресом $ip_address не найден в файле $file_path."
  exit 1
fi

# Удаляем строку с указанным IP-адресом из файла
sed -i "/$ip_address/d" "$file_path"

# Удаляем файл /etc/wireguard/${username}_cl.conf
rm -f "/etc/wireguard/${username}_cl.conf"
rm -f "/etc/wireguard/${username}_privatekey"
rm -f "/etc/wireguard/${username}_publickey"
echo "Пользователь $username с IP-адресом $ip_address был удален из файла $file_path и удален файл /etc/wireguard/${username}_cl.conf"
