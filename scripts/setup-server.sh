#!/bin/bash

# Скрипт для первоначальной настройки сервера Yandex Cloud
# Запускайте этот скрипт на сервере после создания VM

set -e

echo "=== Настройка сервера для деплоя приложения ==="

# Обновление системы
echo "Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Установка Docker
echo "Установка Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker установлен"
else
    echo "✅ Docker уже установлен"
fi

# Установка Docker Compose
echo "Установка Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo apt install docker-compose-plugin -y
    echo "✅ Docker Compose установлен"
else
    echo "✅ Docker Compose уже установлен"
fi

# Установка дополнительных утилит
echo "Установка дополнительных утилит..."
sudo apt install -y curl wget git htop nano

# Создание директории для приложения
echo "Создание директории для приложения..."
mkdir -p ~/persons-app
mkdir -p ~/persons-app/postgres

# Настройка файрволла (если используется ufw)
if command -v ufw &> /dev/null; then
    echo "Настройка файрволла..."
    sudo ufw allow 22/tcp
    sudo ufw allow 8080/tcp
    echo "✅ Файрволл настроен"
fi

# Проверка версий
echo ""
echo "=== Установленные версии ==="
docker --version
docker compose version

echo ""
echo "✅ Настройка сервера завершена!"
echo ""
echo "ВАЖНО: Для применения изменений в группах пользователя, выполните:"
echo "  exit"
echo "  ssh ubuntu@<your-server-ip>"
echo ""
echo "После этого можно настраивать GitHub Actions для автоматического деплоя."
