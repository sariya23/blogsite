#  👾 Сайт-блог
Приложение Django, в котором реализован функционал ведения блога. Можно создавать посты, оставлять комментарии и делиться постами по почте.

Бэкенд почты - это консоль. Все письма будут приходить туда. СУБД - Postgresql.

## 💻 Локальный запуск
*Ниже описаны шаги для запуска проекта через docker-compose*.

Для начала нужно сколнить репозиторий по SSH или HTTP:
- `git clone https://github.com/sariya23/blogsite.git` - HTTP;
- `git clone git@github.com:sariya23/blogsite.git` - SSH.
  
Далее нужно создать файл `.env` в корне проекта и там прописать переменные окружения, как в примере `.env.examples`.
- `SECRET_KEY` - секретный ключ от приложения Django. Можно сгенерировать любую строку;
- `DB_NAME` - название базы данных в Postgresql. Можно придумать любую;
- `DB_USERNAME` - имя пользователя в базе данных. Любая строка;
- `DB_PASSWORD` - пароль от пользователя. Хоть 1234.
- `DB_HOST` - это хост от БД. Если будете запускать локально, то нужно указать `"localhost"`. Если же через Docker, то `"db"`;
- `ALLOWED_HOSTS` - список доступных хостов. Можно взять как в примере.

После того, как переменные созданы, в корне проекта нужно выполнить следующие команды для запуска контейнров:

```bash
docker-compose up --build -d
docker-compose run django python manage.py migrate
```
Дальше нужно создать суперпользователя для доступа в админку:
```bash
docker-compose run django python manage.py createsuperuser
```
*Cледуйте инструкциям на экране*

Теперь запускаем сервер с проектом:
```bash
docker-compose run --service-ports django python manage.py runserver 0.0.0.0:8000
```
Теперь приложение работает по IP 127.0.0.1 и порту 8000
