# Foodgram

![Foodgram workflow](https://github.com/Kirillk/foodgram/actions/workflows/main.yml/badge.svg)

## Ссылки

- **Сайт:** https://foodgram.indevs.in
- **Админка:** https://foodgram.indevs.in/admin/
- **API:** https://foodgram.indevs.in/api/
- **Документация API (ReDoc):** https://foodgram.indevs.in/api/docs/

## Описание проекта

Foodgram — это платформа для публикации рецептов, подписки на авторов и формирования списка покупок. Проект создан в рамках обучения в Яндекс Практикуме и представляет собой полноценное веб-приложение с backend на Django и frontend на React.

### Функциональность

- Регистрация и авторизация по токену
- Просмотр, создание, редактирование и удаление рецептов
- Загрузка изображений блюд в формате Base64
- Теги и ингредиенты для рецептов
- Фильтрация рецептов по тегам, автору, избранному и списку покупок
- Подписка на авторов и просмотр их рецептов
- Добавление рецептов в избранное
- Формирование списка покупок и скачивание его в формате TXT
- Короткие ссылки на рецепты
- Административная панель для управления контентом

## Стек технологий

- **Backend:** Python 3.12, Django, Django REST Framework, Djoser
- **База данных:** PostgreSQL 15
- **Frontend:** React
- **Веб-сервер:** Nginx
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Хранение образов:** Docker Hub
- **SSL:** Let's Encrypt

## Развёртывание проекта

### Требования

- Docker и Docker Compose
- Git

### Локальный запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Kirillk/foodgram.git
cd foodgram
```

2. Создайте файл `.env` в корне проекта (см. раздел «Настройка переменных окружения»).

3. Запустите контейнеры:

```bash
docker compose up -d --build
```

4. Выполните миграции:

```bash
docker compose exec backend python manage.py migrate
```

5. Создайте суперпользователя:

```bash
docker compose exec backend python manage.py createsuperuser
```

6. Соберите статику:

```bash
docker compose exec backend python manage.py collectstatic --noinput
```

7. Сайт доступен по адресу http://localhost:7000/

### Развёртывание на сервере

Проект разворачивается автоматически через GitHub Actions при каждом пуше в ветку `main`:

1. Собираются образы backend, frontend и nginx.
2. Образы публикуются в Docker Hub.
3. На сервере выполняется `docker compose pull` и `up -d`.
4. Применяются миграции и собирается статика.

Для ручного деплоя на сервере:

```bash
cd ~/foodgram
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
```

## Загрузка тестовых данных

В проекте есть management-команда для загрузки ингредиентов из CSV-файла:

```bash
docker compose exec backend python manage.py load_ingredients /app/data/ingredients.csv
```

**Ожидаемый вывод:**

```
Создано: 1378, пропущено: 808
```

Файл `data/ingredients.csv` должен находиться внутри `backend/` — тогда он попадёт в Docker-образ.

## Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=your_strong_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=foodgram.indevs.in,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://foodgram.indevs.in
```

**Описание переменных:**

| Переменная | Описание |
|------------|----------|
| `POSTGRES_DB` | Имя базы данных |
| `POSTGRES_USER` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL |
| `DB_HOST` | Хост базы данных (`db` в Docker) |
| `DB_PORT` | Порт базы данных |
| `SECRET_KEY` | Секретный ключ Django |
| `DEBUG` | Режим отладки (`True` локально, `False` на проде) |
| `ALLOWED_HOSTS` | Разрешённые хосты через запятую |
| `CSRF_TRUSTED_ORIGINS` | Доверенные источники для CSRF |

## Документация API

Полная документация доступна по адресу:

**https://foodgram.indevs.in/api/docs/**

Также доступна OpenAPI-схема:

**https://foodgram.indevs.in/api/schema/**

## Автор

**Telegram:** [@kiyrer](https://t.me/kiyrer)

**GitHub:** [Kirullk](https://github.com/Kirullk)

## Лицензия

Проект создан в учебных целях.