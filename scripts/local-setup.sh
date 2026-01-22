#!/bin/bash

# Скрипт для настройки локального окружения разработки

set -e

echo "=== Настройка локального окружения ==="

# Проверка наличия Python
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 не найден. Пожалуйста, установите Python 3.12"
    exit 1
fi

echo "✅ Python $(python3.12 --version) найден"

# Установка UV
echo "Установка UV..."
if ! command -v uv &> /dev/null; then
    pip install uv
    echo "✅ UV установлен"
else
    echo "✅ UV уже установлен"
fi

# Установка зависимостей
echo "Установка зависимостей проекта..."
uv sync

# Создание .env файла
if [ ! -f .env ]; then
    echo "Создание .env файла..."
    cat > .env << EOF
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=program
DB_PASSWORD=test
DB_NAME=persons

# Application configuration
APP_PORT=8080
EOF
    echo "✅ Файл .env создан"
else
    echo "✅ Файл .env уже существует"
fi

# Запуск PostgreSQL в Docker
echo "Запуск PostgreSQL..."
docker-compose up -d postgres

echo ""
echo "✅ Локальное окружение настроено!"
echo ""
echo "Для запуска приложения:"
echo "  uv run fastapi dev app/presentation/api/main.py"
echo ""
echo "Для запуска тестов:"
echo "  uv run pytest tests/ -v"
echo ""
echo "Для запуска полного стека (с приложением в Docker):"
echo "  docker-compose up"
