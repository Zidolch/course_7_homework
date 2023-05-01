Course 7 homework \
todo list \
`python3.10`, `Django4.1.7`, `Postgres:14.6-alpine`

Установка зависимостей: \
`poetry install`

Список необходимых переменных окружения в `env_example`

Поднять контейнер с базой: \
`docker-compose up -d`

Создать и накатить миграции: \
`python ./manage.py makemigrations` \
`python ./manage.py migrate`

Приложения:
- core: содержит пользователей и авторизацию
- goals: содержит доски, категории, цели и комментарии
- bot: содержит телеграмм-бота