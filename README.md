# Auth System (JWT + RBAC)

## Описание

Реализована backend-система аутентификации и авторизации без использования стандартной Django auth.

Используется JWT для аутентификации и собственная RBAC-модель для управления доступом.

---

## Функционал

### Аутентификация

* Регистрация пользователя
* Вход (login) по email и паролю
* Генерация JWT токена
* Middleware для обработки токена
* Выход (logout) с инвалидированием токена, реализован через blacklist JWT токенов
* Пароли хешируются через bcrypt

---

### Авторизация (RBAC)

- RBAC (Role-Based Access Control)
- Пользователь может иметь несколько ролей
- Гибкая система прав доступа через таблицы:
  - roles
  - user_roles
  - business_elements
  - access_role_rules

Реализованы следующие сущности:

* User
* Role
* UserRole (связь пользователь ↔ роль)
* BusinessElement (ресурсы)
* AccessRoleRule (права доступа)

Права задаются для роли на конкретный ресурс:

* read
* create
* update
* delete

Если хотя бы одна роль пользователя разрешает действие — доступ предоставляется.

---

### Middleware

Кастомный middleware:

* извлекает JWT из заголовка Authorization
* декодирует токен
* определяет пользователя
* сохраняет в request.custom_user

---

##  Безопасность

- Хеширование паролей через bcrypt
- JWT токены (HS256)
- Middleware для проверки авторизации
- Blacklist для logout

---

## API

### Auth

* POST /api/register/
* POST /api/login/
* POST /api/logout/

### Тест

* GET /api/test/

### Пример защищённого ресурса

* GET /api/orders/

---

### Admin API

* POST /api/admin/create-role/
* POST /api/admin/create-element/
* POST /api/admin/set-permission/
* POST /api/admin/assign-role/

---

## База данных

PostgreSQL

Основные таблицы:

* User — пользователь системы
* Role — роли пользователей
* UserRole — связь пользователей и ролей
* BusinessElement — бизнес-сущности (orders, и т.д.)
* AccessRoleRule — правила доступа
* blacklisted_tokens — blacklist JWT токенов

---

## Запуск

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Настроить PostgreSQL в settings.py

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## Примечание

JWT передаётся в заголовке:

Authorization: Bearer <token>
