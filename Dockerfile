# Используем базовый образ Ubuntu
FROM ubuntu:latest

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip wireguard-tools curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем виртуальный сетевой интерфейс eth0 внутри контейнера
RUN ip link add dev ens18 type dummy || true

# Настраиваем IP-адрес для виртуального интерфейса eth0
RUN ip addr add 192.168.1.100/24 dev ens18 || true

# Включаем виртуальный интерфейс eth0
RUN ip link set dev ens18 up || true

# Устанавливаем переменную среды для корректной работы Python внутри контейнера
ENV LANG C.UTF-8

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта в контейнер
COPY . .

# Настраиваем переменные окружения, если необходимо
ENV VARIABLE_NAME=value

# Запускаем команду для запуска вашего телеграм бота
CMD ["python3", "main.py"]
