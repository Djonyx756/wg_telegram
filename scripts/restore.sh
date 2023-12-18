#!/bin/bash

# Получение пути к директории, в которой находится скрипт restore.sh
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Путь и имя архива
BACKUP_FILE="$SCRIPT_DIR/../reset/wg0_backup.zip"

# Директория для распаковки
DESTINATION_DIR="/etc/wireguard/"

# Проверка наличия архива
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Архив $BACKUP_FILE не найден."
  exit 1
fi

# Удаляем все файлы из директории назначения
rm -rf "$DESTINATION_DIR"/*

# Переходим в директорию назначения
cd "$DESTINATION_DIR"

# Распаковываем архив
unzip -j "$BACKUP_FILE"

# Проверка наличия распакованного файла
if [ ! -f "$DESTINATION_DIR/cofigs.txt" ]; then
  echo "Распакованный файл cofigs.txt не найден в директории $DESTINATION_DIR."
  exit 1
fi

# Перемещаем файл cofigs.txt
mv cofigs.txt "$SCRIPT_DIR"/..

wg-quick down wg0
wg-quick up wg0

