Запуск этого говна:
```bash
docker-compose up --build -d
docker-compose run django python manage.py makemigrations
docker-compose run django python manage.py migrate
docker-compose run --service-ports django python manage.py runserver 0.0.0.0:8000
```