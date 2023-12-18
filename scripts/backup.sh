#!/bin/bash

# Путь к исходной директории
SOURCE_DIR="/etc/wireguard/"

# Получение пути к директории, в которой находится скрипт backup.sh
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Путь и имя архива
BACKUP_FILE="$SCRIPT_DIR/../reset/wg0_backup.zip"

# Проверяем, существует ли архив
if [[ -f "$BACKUP_FILE" ]]; then
  # Архив существует, удаляем его
  rm "$BACKUP_FILE"
fi

# Создаем новый архив
zip -r "$BACKUP_FILE" "$SOURCE_DIR"

# Переходим в директорию с исходными файлами перед добавлением дополнительных файлов
cd "$SOURCE_DIR"

# Добавляем файл cofigs.txt в архив без сохранения пути
zip -j "$BACKUP_FILE" "$SCRIPT_DIR/../cofigs.txt"

wg-quick down wg0
wg-quick up wg0

