# 💰 Finance Tracker API

REST API для учета личных финансов: доходы, расходы, категории и аналитика.

---

## 🚀 Стек

* Python 3.13
* FastAPI
* SQLAlchemy
* SQLite
* JWT (аутентификация)
* Pytest (тесты)

---

## 📦 Функциональность

### 🔐 Аутентификация

* Регистрация пользователя
* Логин (JWT)
* Получение текущего пользователя (`/auth/me`)

### 📁 Категории

* Создание категории (income / expense)
* Получение списка категорий

### 💸 Транзакции

* Создание транзакции
* Получение списка транзакций
* Фильтрация:

  * по типу
  * по категории
  * по дате

### 🧠 Бизнес-логика

* Нельзя создать транзакцию с типом, отличным от категории
* Пользователь видит только свои данные

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <https://github.com/ScandicCon/finance-tracker-api>
cd finance-tracker-api
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустить сервер

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Запуск тестов

```bash
pytest
```

---

## 📡 Основные endpoints

### Auth

* `POST /auth/register`
* `POST /auth/login`
* `GET /auth/me`

### Categories

* `POST /categories/`
* `GET /categories/`

### Transactions

* `POST /transactions/`
* `GET /transactions/`

---

## 🔐 Авторизация

Используется JWT.

Заголовок:

```text
Authorization: Bearer <token>
```

---

## 📊 Пример запроса

```json
POST /transactions/

{
  "amount": "500.00",
  "type": "expense",
  "category_id": 1,
  "description": "Lunch",
  "date": "2026-04-26"
}
```

---

## 📁 Структура проекта

```text
app/
├── models/
├── schemas/
├── routers/
├── db/
├── core/
└── main.py

tests/
```

---

## ✅ Что реализовано

* JWT авторизация
* CRUD операции
* Связи между таблицами
* Валидация данных
* Тесты (auth, categories, transactions)

---

## 🎯 Цель проекта

Пет-проект для демонстрации навыков backend-разработки:

* FastAPI
* работа с БД
* архитектура
* тестирование

---

## 👨‍💻 Автор

Даниил
