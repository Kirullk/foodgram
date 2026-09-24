# Foodgram — сайт рецептов

## О проекте

Foodgram — это платформа для публикации рецептов, подписки на авторов и формирования списка покупок. Пользователи могут создавать рецепты с ингредиентами и тегами, добавлять чужие рецепты в избранное и корзину, а также скачивать сводный список покупок в текстовом формате.

## Адрес проекта

Проект запущен на сервере и доступен по адресу:

**http://81.26.178.46**

Также проект доступен по доменному имени:

**https://foodgram.indevs.in**

Административная панель Django:

**https://foodgram.indevs.in/admin/**

API проекта:

**https://foodgram.indevs.in/api/**

Документация API (Redoc):

**https://foodgram.indevs.in/api/docs/**

## Стек технологий

- **Backend:** Python 3.12, Django, Django REST Framework, Djoser
- **База данных:** PostgreSQL 15
- **Frontend:** React
- **Веб-сервер:** Nginx
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Хранение образов:** Docker Hub

## Автор

**Telegram:** [@kiyrer](https://t.me/kiyrer)

---

## Эндпоинты API

### Пользователи

**GET** `/api/users/` — список пользователей (пагинация: `page`, `limit`)

Пример ответа:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "vpupkin@yandex.ru",
            "id": 1,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Иванов",
            "is_subscribed": false,
            "avatar": null
        }
    ]
}
```

**POST** `/api/users/` — регистрация нового пользователя

Пример запроса:
```json
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Иванов",
    "password": "Qwerty123"
}
```

Пример ответа (201):
```json
{
    "email": "vpupkin@yandex.ru",
    "id": 1,
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Иванов"
}
```

**GET** `/api/users/{id}/` — профиль пользователя

**GET** `/api/users/me/` — текущий пользователь (требуется токен)

**PUT** `/api/users/me/avatar/` — загрузка аватара (требуется токен)

Пример запроса:
```json
{
    "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
}
```

**DELETE** `/api/users/me/avatar/` — удаление аватара (требуется токен)

**POST** `/api/users/set_password/` — смена пароля (требуется токен)

Пример запроса:
```json
{
    "new_password": "NewQwerty123",
    "current_password": "Qwerty123"
}
```

### Аутентификация

**POST** `/api/auth/token/login/` — получение токена

Пример запроса:
```json
{
    "email": "vpupkin@yandex.ru",
    "password": "Qwerty123"
}
```

Пример ответа:
```json
{
    "auth_token": "a1b2c3d4e5f6g7h8i9j0"
}
```

**POST** `/api/auth/token/logout/` — удаление токена (требуется токен)

### Подписки

**GET** `/api/users/subscriptions/` — список подписок (требуется токен)

Параметры: `page`, `limit`, `recipes_limit`

**POST** `/api/users/{id}/subscribe/` — подписаться на пользователя (требуется токен)

**DELETE** `/api/users/{id}/subscribe/` — отписаться (требуется токен)

### Теги

**GET** `/api/tags/` — список тегов

Пример ответа:
```json
[
    {
        "id": 1,
        "name": "Завтрак",
        "slug": "breakfast"
    },
    {
        "id": 2,
        "name": "Обед",
        "slug": "lunch"
    }
]
```

**GET** `/api/tags/{id}/` — получение тега

### Ингредиенты

**GET** `/api/ingredients/` — список ингредиентов

Параметры: `name` (поиск по началу названия)

Пример ответа:
```json
[
    {
        "id": 1,
        "name": "Мука пшеничная",
        "measurement_unit": "г"
    },
    {
        "id": 2,
        "name": "Сахар",
        "measurement_unit": "г"
    }
]
```

**GET** `/api/ingredients/{id}/` — получение ингредиента

### Рецепты

**GET** `/api/recipes/` — список рецептов

Параметры:
- `page`, `limit` — пагинация
- `is_favorited` — 0 или 1
- `is_in_shopping_cart` — 0 или 1
- `author` — id автора
- `tags` — slug тегов

Пример ответа:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "Завтрак",
                    "slug": "breakfast"
                }
            ],
            "author": {
                "email": "vpupkin@yandex.ru",
                "id": 1,
                "username": "vasya.pupkin",
                "first_name": "Вася",
                "last_name": "Иванов",
                "is_subscribed": false,
                "avatar": null
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "Мука пшеничная",
                    "measurement_unit": "г",
                    "amount": 300
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Пицца Маргарита",
            "image": "http://foodgram.indevs.in/media/recipes/images/pizza.png",
            "text": "Описание рецепта",
            "cooking_time": 90
        }
    ]
}
```

**POST** `/api/recipes/` — создание рецепта (требуется токен)

Пример запроса:
```json
{
    "tags": [1, 2],
    "ingredients": [
        {
            "id": 1,
            "amount": 300
        }
    ],
    "name": "Пицца Маргарита",
    "image": "data:image/png;base64,iVBORw0KGgo...",
    "text": "Описание рецепта",
    "cooking_time": 90
}
```

**GET** `/api/recipes/{id}/` — получение рецепта

**PATCH** `/api/recipes/{id}/` — обновление рецепта (только автор, требуется токен)

**DELETE** `/api/recipes/{id}/` — удаление рецепта (только автор, требуется токен)

**GET** `/api/recipes/{id}/get-link/` — короткая ссылка на рецепт

Пример ответа:
```json
{
    "short-link": "https://foodgram.indevs.in/s/3d0"
}
```

### Избранное

**POST** `/api/recipes/{id}/favorite/` — добавить в избранное (требуется токен)

**DELETE** `/api/recipes/{id}/favorite/` — удалить из избранного (требуется токен)

### Список покупок

**POST** `/api/recipes/{id}/shopping_cart/` — добавить в корзину (требуется токен)

**DELETE** `/api/recipes/{id}/shopping_cart/` — удалить из корзины (требуется токен)

**GET** `/api/recipes/download_shopping_cart/` — скачать список покупок (требуется токен)

Ответ — файл `shopping_cart.txt` в кодировке UTF-8.

Пример содержимого:
```
Список покупок:

Мука пшеничная. 300 (г)
Сахар. 150 (г)
Яйца куриные. 3 (шт.)
```

---

## Авторизация

Все защищённые эндпоинты требуют заголовок:

```
Authorization: Token a1b2c3d4e5f6g7h8i9j0
```

Токен получается через `POST /api/auth/token/login/`.

---

## Развёртывание

Проект собирается и разворачивается автоматически через GitHub Actions при каждом пуше в репозиторий:

1. Собираются образы backend, frontend и nginx.
2. Образы публикуются в Docker Hub.
3. На сервере выполняется `docker compose pull` и `up -d`.
4. Применяются миграции и собирается статика.