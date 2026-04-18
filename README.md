# Web Course Bookstore (Django Edition)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2%2B-green)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Веб-приложение интернет-магазина книг, реализованное на Django с использованием MySQL. Проект включает полноценный CRUD-каталог с пагинацией и фильтрацией, систему регистрации и авторизации с разграничением прав доступа, корзину на основе сессий (с переносом данных при входе), оформление заказов с сохранением снапшота цен на момент покупки, клиентскую валидацию форм в реальном времени с AJAX-проверками и Selenium-тесты. Приложение полностью контейнеризировано и готово к развертыванию через Docker Compose в связке Nginx + Gunicorn + MySQL.

## Что здесь реализовано?

### Управление каталогом (CRUD)
- Полноценный каталог книг с пагинацией.
- Возможность создания, редактирования и удаления книг через отдельные формы (админ-функционал).
- База данных MySQL.
- Контроль качества кода: настроены Black (форматтер) и Flake8 (линтер).

### Корзина и заказы
- Модели `Cart` / `CartItem`: поддержка гостей через Django Sessions. Если гость добавляет товар, а затем логинится - корзина не теряется, а переносится на аккаунт пользователя.
- Снапшот цен: Модели `Order` / `OrderItem` сохраняют название книги и цену на момент покупки.
- Управление количеством товаров и автоматический пересчет итоговой суммы в корзине.
- Страница истории заказов в профиле пользователя с детализацией состава и дат.

### Безопасность и валидация
- Поддержка нескольких алгоритмов хеширования паролей: **PBKDF2 SHA-256**, **Argon2id** и **bcrypt SHA-256**.
- Клиентская валидация (JavaScript) в реальном времени:
    - Email: проверка по стандарту RFC 5322.
    - Пароль: минимум 6 символов, проверка на совпадение с подтверждением.
    - Динамические сообщения об ошибках без перезагрузки страницы.

### Деплой и инфраструктура
- Docker-контейнеризация: многоступенчатая сборка (multi-stage build) для минимизации размера production-образа.
- Nginx: настроен как прокси-сервер для Gunicorn и раздачи статических файлов.
- Gunicorn: используется в качестве WSGI-сервера в production-окружении.
- Healthcheck: настроена проверка готовности MySQL перед запуском приложения.

## Технологический стек

| Категория       | Технологии                                                                 |
| :-------------- | :-------------------------------------------------------------------------- |
| **Backend**     | Python 3.10+, Django 5.2+                                                   |
| **База данных** | MySQL 8.0                                                                   |
| **Frontend**    | HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API / AJAX)                     |
| **Сервер**      | Gunicorn, Nginx                            |
| **Инфраструктура** | Docker, Docker Compose                                    |
| **Качество кода** | Black, Flake8                                                     |
| **Тестирование**| Selenium                                                |

## Как запустить проект?

Существует два способа запуска: классический для разработки (через `manage.py`) и продакшн-подобный (через Docker).

### Способ 1: Локальный запуск для разработки (Development)

**Предварительные требования:** Python 3.10+, MySQL Server, Git.

1.  **Клонирование и виртуальное окружение:**
    ```bash
    git clone https://github.com/meh-w/web-course-bookstore.git
    cd web-course-bookstore
    python -m venv venv
    source venv/bin/activate  # для Windows: venv\Scripts\activate

2.  **Установка зависимостей:**
    ```bash
    pip install -r requirements/dev.txt

3.  **Настройка подключения к MySQL:**
    Создайте базу данных bookstore_db в вашем MySQL и пропишите доступы в файле .env или settings.py.
    ```bash
    # Пример структуры .env файла
    DB_NAME=bookstore_db
    DB_USER=root
    DB_PASSWORD=yourpass
    DB_HOST=localhost
    DB_PORT=3306

4.  **Применение миграций и загрузка тестовых данных:**
   
    Заполните базу данных тестовыми данными, затем примените команды.
    ```bash
    python manage.py migrate
    python manage.py createsuperuser 

5.  **Запуск сервера:**
    ```bash
    python manage.py runserver
  Приложение будет доступно по адресу: http://127.0.0.1:8000

### Способ 2: Запуск через Docker
1. Убедитесь, что Docker и Docker Compose установлены.

2. **Запустите сборку и контейнеры:**
    ```bash
    docker-compose up --build -d

3. **Применение миграций (внутри контейнера):**
  ```bash
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py createsuperuser
  docker-compose exec web python manage.py collectstatic --noinput
  ```

4. **запуск сервера:**
  Приложение будет проксироваться через Nginx на порту 80. Перейдите на http://localhost.
