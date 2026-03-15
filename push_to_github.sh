#!/bin/bash
# Скрипт для публикации Syndi на GitHub
# Использование: ./push_to_github.sh

set -e

REPO_URL="https://github.com/donjonson-hash/Syndi.git"
PROJECT_DIR="/mnt/okcomputer/output/syndi"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🚀 Публикация Syndi на GitHub                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd "$PROJECT_DIR"

# Проверяем, инициализирован ли git
if [ -d ".git" ]; then
    echo "✅ Git уже инициализирован"
else
    echo "🔧 Инициализация Git..."
    git init
    echo "✅ Git инициализирован"
fi

echo ""
echo "📋 Конфигурация Git..."

# Проверяем настроен ли user.name
if ! git config user.name > /dev/null 2>&1; then
    echo "⚠️  Git user.name не настроен"
    read -p "Введите ваше имя для Git: " git_name
    git config user.name "$git_name"
fi

# Проверяем настроен ли user.email
if ! git config user.email > /dev/null 2>&1; then
    echo "⚠️  Git user.email не настроен"
    read -p "Введите ваш email для Git: " git_email
    git config user.email "$git_email"
fi

echo "✅ Git настроен:"
echo "   Name: $(git config user.name)"
echo "   Email: $(git config user.email)"

echo ""
echo "📁 Добавление файлов..."
git add .

echo ""
echo "💾 Создание коммита..."
git commit -m "Initial commit: Syndi MVP with DeepSeek integration

Features:
- Big Five Assessment (15 questions, OCEAN model)
- Smart Matching Algorithm (Skills + Personality + Goals)
- AI Agent Architecture with memory
- Kristina - UX Designer Agent
- DeepSeek API integration
- FastAPI backend (18 endpoints)
- 36 unit tests

Co-authored-by: Kimi (AI-partner)"

echo ""
echo "🔗 Добавление remote origin..."
if git remote | grep -q "origin"; then
    echo "📝 Обновление remote origin..."
    git remote set-url origin "$REPO_URL"
else
    git remote add origin "$REPO_URL"
fi

echo ""
echo "⬆️  Push на GitHub..."
echo "   URL: $REPO_URL"
echo ""

# Пробуем push
git branch -M main

if git push -u origin main; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║          ✅ Успешно опубликовано!                              ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "   📁 Репозиторий: $REPO_URL"
    echo ""
    echo "   Следующие шаги:"
    echo "   1. Перейдите на https://github.com/donjonson-hash/Syndi"
    echo "   2. Проверьте, что все файлы загружены"
    echo "   3. Настройте GitHub Secrets для CI/CD (опционально)"
    echo ""
else
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║          ❌ Ошибка при push                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "   Возможные причины:"
    echo "   1. Нет доступа к репозиторию"
    echo "   2. Нужна аутентификация GitHub"
    echo "   3. Репозиторий не существует"
    echo ""
    echo "   Решение:"
    echo "   1. Создайте репозиторий на GitHub:"
    echo "      https://github.com/new"
    echo "   2. Назовите его 'Syndi'"
    echo "   3. Не добавляйте README (уже есть)"
    echo "   4. Запустите скрипт снова"
    echo ""
    exit 1
fi
