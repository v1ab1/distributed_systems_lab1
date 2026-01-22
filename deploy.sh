#!/bin/bash

# Скрипт для ручного деплоя на сервер Yandex Cloud
# Использование: ./deploy.sh

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Деплой приложения Persons на Yandex Cloud ===${NC}"

# Проверка переменных окружения
if [ -z "$SERVER_HOST" ]; then
    echo -e "${RED}Ошибка: SERVER_HOST не установлен${NC}"
    exit 1
fi

if [ -z "$SERVER_USER" ]; then
    echo -e "${RED}Ошибка: SERVER_USER не установлен${NC}"
    exit 1
fi

echo -e "${YELLOW}Сервер: $SERVER_USER@$SERVER_HOST${NC}"

# Сборка Docker образа
echo -e "${GREEN}Шаг 1: Сборка Docker образа${NC}"
docker build -t persons-app:latest .

# Сохранение образа в tar
echo -e "${GREEN}Шаг 2: Сохранение образа${NC}"
docker save persons-app:latest | gzip > persons-app.tar.gz

# Копирование файлов на сервер
echo -e "${GREEN}Шаг 3: Копирование файлов на сервер${NC}"
scp persons-app.tar.gz $SERVER_USER@$SERVER_HOST:~/
scp docker-compose.prod.yml $SERVER_USER@$SERVER_HOST:~/persons-app/docker-compose.yml
scp -r postgres $SERVER_USER@$SERVER_HOST:~/persons-app/

# Деплой на сервере
echo -e "${GREEN}Шаг 4: Деплой на сервере${NC}"
ssh $SERVER_USER@$SERVER_HOST << 'ENDSSH'
    set -e
    
    cd ~/persons-app
    
    # Загрузка образа
    docker load < ~/persons-app.tar.gz
    
    # Создание .env файла (если нужно)
    if [ ! -f .env ]; then
        cat > .env << EOF
POSTGRES_USER=program
POSTGRES_PASSWORD=test
POSTGRES_DB=persons
APP_PORT=8080
DOCKER_IMAGE=persons-app:latest
EOF
    fi
    
    # Перезапуск контейнеров
    docker-compose down || true
    docker-compose up -d
    
    # Очистка
    rm -f ~/persons-app.tar.gz
    
    echo "Деплой завершен успешно!"
ENDSSH

# Очистка локальных файлов
echo -e "${GREEN}Шаг 5: Очистка${NC}"
rm -f persons-app.tar.gz

echo -e "${GREEN}=== Деплой завершен успешно! ===${NC}"
echo -e "${YELLOW}Приложение доступно по адресу: http://$SERVER_HOST:8080${NC}"
