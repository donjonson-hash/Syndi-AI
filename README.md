# Syndi - AI-напарник для мировых проектов

<p align="center">
  <strong>Платформа персональных AI-агентов для глобального профессионального сотрудничества</strong>
</p>

## 🎯 О проекте

**Syndi** (Synergy + Individual) — это платформа, которая соединяет профессионалов по всему миру на основе их психотипа и навыков. Каждый пользователь получает персонального AI-агента, который помогает находить идеальных партнёров для проектов.

### Ключевые особенности

- 🧠 **Big Five Assessment** — научно обоснованная оценка личности (OCEAN)
- 🤝 **Smart Matching** — алгоритм совместимости по психотипу и навыкам
- 🤖 **AI-агенты** — персональные помощники с DeepSeek API
- 🔌 **DeepSeek Integration** — умные ответы от LLM
- 🌍 **Глобальная сеть** — работа с профессионалами из любой точки мира

### 🎉 Новое: DeepSeek API Integration

Кристина теперь использует **DeepSeek API** для генерации умных, контекстуальных ответов!

```bash
# Пример диалога с Кристиной
curl -X POST "http://localhost:8000/agents/kristina_ux_001/chat?user_id=123" \
  -H "Content-Type: application/json" \
  -d '{"message": "Как провести исследование пользователей?"}'

# Ответ (через DeepSeek API):
# "Отличный вопрос! Исследования пользователей — это фундамент хорошего продукта.
#  Давай разберём по шагам...
```

**Особенности:**
- ✅ Структурированные ответы с конкретными рекомендациями
- ✅ Адаптация под контекст (стартап, MVP)
- ✅ Практические советы из реального опыта
- ✅ Fallback на шаблоны при недоступности API

## 🏗️ Архитектура

```
syndi/
├── api/              # FastAPI endpoints
│   └── main.py       # Главное приложение
├── agents/           # AI-агенты
│   ├── base.py       # Базовый класс агента
│   ├── kristina.py   # Кристина — UX-дизайнер
│   └── personalities/# Личности агентов
├── models/           # Pydantic модели
│   ├── big_five.py   # Модель Big Five
│   └── user.py       # Модели пользователей
├── services/         # Бизнес-логика
│   └── matching.py   # Алгоритм матчинга
├── tests/            # Тесты
│   ├── test_big_five.py
│   ├── test_matching.py
│   └── test_agents.py
├── docs/             # Документация
├── requirements.txt  # Зависимости
└── README.md         # Этот файл
```

## 🚀 Быстрый старт

### Установка

```bash
# Клонировать репозиторий
git clone <repository-url>
cd syndi

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt
```

### Запуск API

```bash
# Запуск сервера разработки
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступно по адресу: http://localhost:8000

- Документация Swagger: http://localhost:8000/docs
- Документация ReDoc: http://localhost:8000/redoc

## 🔌 Настройка DeepSeek API (Опционально)

Для получения умных ответов от Кристины:

```bash
# 1. Получите API ключ на https://platform.deepseek.com/
# 2. Создайте .env файл
cp .env.example .env

# 3. Добавьте ключ в .env
DEEPSEEK_API_KEY=sk-your-api-key-here

# 4. Установите aiohttp
pip install aiohttp==3.9.1
```

**Бесплатно:** 10M токенов для новых пользователей!

Подробнее: [docs/DEEPSEEK_SETUP.md](docs/DEEPSEEK_SETUP.md)

## 📚 API Endpoints

### Big Five Test

| Method | Endpoint | Описание |
|--------|----------|----------|
| GET | `/test/questions` | Получить 15 вопросов теста |
| POST | `/test/submit` | Отправить ответы, получить профиль |

### Users

| Method | Endpoint | Описание |
|--------|----------|----------|
| POST | `/users` | Создать пользователя |
| GET | `/users/{id}` | Получить профиль |
| PATCH | `/users/{id}` | Обновить профиль |
| POST | `/users/{id}/big-five` | Сохранить результаты теста |
| GET | `/users` | Список пользователей |

### Matching

| Method | Endpoint | Описание |
|--------|----------|----------|
| GET | `/matches/{user_id}` | Найти совместимых пользователей |
| GET | `/matches/{user_id}/quick` | Быстрый матчинг (MVP) |

### Development

| Method | Endpoint | Описание |
|--------|----------|----------|
| POST | `/seed` | Создать тестовые данные |

### AI Agents

| Method | Endpoint | Описание |
|--------|----------|----------|
| GET | `/agents` | Список доступных агентов |
| GET | `/agents/{agent_id}` | Информация об агенте |
| POST | `/agents/{agent_id}/chat` | Отправить сообщение агенту |
| GET | `/agents/{agent_id}/history/{user_id}` | История общения |
| DELETE | `/agents/{agent_id}/history/{user_id}` | Очистить историю |

## 🧪 Big Five Тест

### Структура теста

Тест состоит из **15 вопросов** (по 3 на каждую черту OCEAN):

| Черта | Описание | Вопросы |
|-------|----------|---------|
| **O** - Openness | Открытость опыту | 1-3 |
| **C** - Conscientiousness | Добросовестность | 4-6 |
| **E** - Extraversion | Экстраверсия | 7-9 |
| **A** - Agreeableness | Доброжелательность | 10-12 |
| **N** - Neuroticism | Нейротизм | 13-15 |

### Шкала ответов

- 1 — Полностью не согласен
- 2 — Не согласен
- 3 — Нейтрально
- 4 — Согласен
- 5 — Полностью согласен

### Пример использования

```bash
# Получить вопросы
curl http://localhost:8000/test/questions

# Отправить ответы
curl -X POST http://localhost:8000/test/submit \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_id": 1, "value": 4},
      {"question_id": 2, "value": 5},
      ...
      {"question_id": 15, "value": 3}
    ]
  }'
```

## 🤝 Алгоритм матчинга

### Факторы совместимости

```
Overall Score = Skill × 0.4 + Personality × 0.35 + Goals × 0.25
```

#### 1. Совместимость навыков (40%)
- Ищем **комплементарность** — разные, но совместимые навыки
- Небольшой бонус за общие навыки (общее понимание)

#### 2. Совместимость личности (35%)
- Основана на модели **Big Five**
- Похожие значения для Openness и Conscientiousness
- Высокая Agreeableness у обоих = лучше
- Низкий Neuroticism у обоих = лучше

#### 3. Совместимость целей (25%)
- Совпадающие цели дают максимальный балл
- Совместимые пары (например, FIND_COFOUNDER ↔ JOIN_PROJECT)

### Пример результата матчинга

```json
{
  "user_id": "...",
  "total_matches": 3,
  "matches": [
    {
      "user": {
        "name": "Мария Иванова",
        "title": "UX Designer",
        "skills": [...]
      },
      "scores": {
        "overall": 78.5,
        "skill": 82.0,
        "personality": 75.3,
        "goal": 80.0
      },
      "complementary_skills": ["Figma", "User Research"],
      "shared_interests": ["AI", "Startups"]
    }
  ]
}
```

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest

# Запустить с покрытием
pytest --cov=.

# Запустить конкретный файл тестов
pytest tests/test_big_five.py
pytest tests/test_matching.py
```

## 🤖 AI-Агенты

### Кристина — UX Designer Agent

**Кристина** — первый AI-агент в экосистеме Syndi. Она профессиональный UX-дизайнер с 8-летним опытом.

#### Возможности Кристины:
- 🎨 **UX/UI консультации** — советы по дизайну интерфейсов
- 🔍 **User Research** — помощь в исследованиях пользователей
- 📐 **Prototyping** — рекомендации по прототипированию
- 🧪 **Usability Testing** — планирование юзабилити-тестов
- 📚 **Design Systems** — создание дизайн-систем

#### Пример общения с Кристиной:

```bash
# Получить информацию об агенте
curl http://localhost:8000/agents/kristina_ux_001

# Отправить сообщение
curl -X POST http://localhost:8000/agents/kristina_ux_001/chat?user_id=123 \
  -H "Content-Type: application/json" \
  -d '{"message": "Как провести исследование пользователей?"}'
```

**Ответ Кристины:**
```json
{
  "agent_id": "kristina_ux_001",
  "agent_name": "Кристина",
  "content": "Отлично, что думаешь об исследовании! Это фундамент хорошего дизайна...",
  "message_type": "advice",
  "suggestions": [
    "Провести интервью с пользователями",
    "Создать user personas",
    "Составить CJM"
  ],
  "actions": [
    {"type": "suggest", "label": "Получить совет", "payload": "advice"},
    {"type": "share", "label": "Поделиться дизайном", "payload": "share_design"}
  ]
}
```

### Архитектура агентов

Каждый агент имеет:
- **Память** — сохраняет контекст разговора
- **Профиль** — знает Big Five пользователя
- **Контекст проекта** — понимает над чем работает пользователь
- **Экспертизу** — специализированные знания в своей области

### Будущие агенты

| Агент | Роль | Статус |
|-------|------|--------|
| **Кристина** | UX Designer | ✅ Готово |
| **Алексей** | Full-stack Developer | 🚧 В планах |
| **Мария** | Product Manager | 🚧 В планах |
| **Дмитрий** | Marketing | 🚧 В планах |

## 📋 Roadmap

### MVP (Месяц 1) ✅
- [x] Big Five тест (15 вопросов)
- [x] Базовый алгоритм матчинга
- [x] FastAPI endpoints
- [x] AI-агент Кристина (UX Designer)
- [ ] Telegram-бот интерфейс

### Beta (Месяцы 2-3)
- [ ] Flutter мобильное приложение
- [ ] PostgreSQL база данных
- [ ] Рабочие пространства (Kanban, чаты)
- [ ] 1000 тестовых пользователей

### Launch (Месяцы 4-6)
- [ ] Платёжная система
- [ ] AI-агенты на основе DeepSeek API
- [ ] Enterprise клиенты
- [ ] Международные команды

## 💼 Бизнес-модель

| Тариф | Цена | Возможности |
|-------|------|-------------|
| **Free** | $0 | Профиль, 3 матча/день |
| **Pro** | $9/мес | Безлимит матчинг, AI-агент, 3 проекта |
| **Team** | $29/мес | Командные пространства, API |
| **Enterprise** | Custom | White-label, приоритет |

## 🤝 Contributing

Мы приветствуем вклад в развитие проекта! 

1. Fork репозитория
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 👥 Команда

- **Anatoly** — Founder & Product
- **Kimi** — AI-партнёр разработки

---

<p align="center">
  <strong>Syndi — найди своего идеального партнёра для следующего большого проекта!</strong>
</p>
