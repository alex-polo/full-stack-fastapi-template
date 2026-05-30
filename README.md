# Full-Stack FastAPI Template

Полноценный шаблон для создания современного full-stack приложения на базе FastAPI и React с использованием лучших практик разработки.

## 📋 Описание

Этот шаблон предоставляет готовую архитектуру для быстрого старта проекта с:

- **Backend**: FastAPI с SQLAlchemy, Celery, Pydantic, Alembic
- **Frontend**: React + TypeScript + Vite с Material-UI
- **DevOps**: Docker, Docker Compose, pre-commit hooks
- **Monitoring**: Sentry для отслеживания ошибок
- **Testing**: pytest с покрытием кода

## 🛠 Технологический стек

### Backend

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **Celery** - асинхронная задача и брокер сообщений
- **Pydantic** - валидация данных и сериализация
- **Alembic** - миграции базы данных
- **Redis** - брокер сообщений для Celery
- **Sentry** - мониторинг и отладка ошибок
- **Pytest** - тестирование

### Frontend

- **React 19** - библиотека для создания пользовательских интерфейсов
- **TypeScript** - статическая типизация
- **Vite** - инструмент сборки
- **Material-UI** - компоненты для React
- **React Router** - маршрутизация
- **TanStack Query** - управление состоянием и кеширование
- **React Hook Form** - управление формами
- **Zod** - валидация схем

### DevOps

- **Docker** - контейнеризация
- **Docker Compose** - оркестрация контейнеров
- **Pre-commit** - автоматическая проверка кода
- **Ruff** - линтер и форматтер для Python
- **ESLint** - линтер для JavaScript/TypeScript

## 📦 Установка

### Предварительные требования

- Python 3.14+
- Node.js 20+
- Docker и Docker Compose
- Git

### Клонирование репозитория

```bash
git clone https://github.com/alex-polo/full-stack-fastapi-template.git
cd full-stack-fastapi-template
```

### Установка зависимостей

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd client
npm install
```

## 🚀 Запуск

### Вариант 1: Использование Docker

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down
```

### Вариант 2: Локальный запуск

#### Backend

```bash
cd backend

# Активация виртуального окружения
source .venv/bin/activate

# Запуск в режиме разработки
python run_dev.py

# Или запуск в режиме производства
python run_main.py
```

#### Frontend

```bash
cd client

# Запуск в режиме разработки
npm run dev

# Сборка для производства
npm run build
```

## 🛠 Разработка

### Pre-commit hooks

Проект использует pre-commit для автоматической проверки кода перед коммитом. Установите hooks:

```bash
pre-commit install
```

Доступные проверки:

- **Ruff** - форматирование и проверка кода Python
- **Mypy** - статический анализ типов
- **ESLint** - проверка JavaScript/TypeScript кода
- **Prettier** - форматирование файлов

### Тестирование

```bash
# Запуск всех тестов
pytest

# С запуском покрытия
pytest --cov=src

# С определенным тестом
pytest tests/test_example.py
```

### Миграции базы данных

```bash
cd backend

# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Основные переменные:

- `DATABASE_URL` - строка подключения к базе данных
- `REDIS_URL` - URL для Redis
- `SENTRY_DSN` - DSN для Sentry
- `JWT_SECRET_KEY` - секретный ключ для JWT
- `CORS_ORIGINS` - разрешенные origins для CORS

### Docker Compose

Файл `compose.yml` содержит конфигурацию для:

- Backend API
- Frontend React
- PostgreSQL
- Redis
- Nginx (для проксирования)
