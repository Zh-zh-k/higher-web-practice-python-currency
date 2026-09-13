# Currency Service

REST API сервис для работы с курсами валют.

Проект включает:

- FastAPI API;
- PostgreSQL;
- Scrapy parser;
- JWT-авторизацию;
- Docker Compose.

## Возможности

Сервис поддерживает:

- регистрацию пользователей;
- авторизацию по JWT;
- обновление access token через refresh token;
- получение списка валют;
- получение последнего курса валюты;
- получение истории курса за период;
- получение полной истории курса.

Данные о курсах валют загружаются с сайта ЦБ РФ с помощью Scrapy.

## Запуск

Создайте файл `.env` на основе `.env.example`.

Запустите сервис командой:

`docker compose up -d --build`

После запуска Swagger будет доступен по адресу:

[http://localhost:8000/docs](http://localhost:8000/docs)

## Состав сервиса

Сервис состоит из:

- FastAPI API;
- PostgreSQL;
- Scrapy parser.

Парсер автоматически запускается при старте контейнера и повторяется раз в 24 часа.

## Основные эндпоинты

### Users

- `POST /users/register` — регистрация пользователя;
- `GET /users/{user_id}` — получение пользователя по ID;
- `GET /users/email/{email}` — получение пользователя по email;
- `PUT /users` — обновление данных пользователя.

### Auth

- `POST /auth/login` — авторизация пользователя;
- `POST /auth/refresh` — обновление токенов.

### Currency

- `GET /currencies` — список валют;
- `GET /currencies/{currency_code}` — последний курс валюты;
- `GET /currencies/{currency_code}/history` — история курса за период;
- `GET /currencies/{currency_code}/all` — полная история курса.

Все эндпоинты валют и защищённые эндпоинты пользователей требуют Bearer access token.

## Парсер

Scrapy-парсер получает данные с сайта ЦБ РФ:

`http://www.cbr.ru/scripts/XML_daily.asp`

При каждом запуске парсер загружает курсы за последние 10 дней и сохраняет их в PostgreSQL.

Повторные записи для одной валюты на одну дату не создаются.