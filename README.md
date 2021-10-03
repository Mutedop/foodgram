##Foodgram
«Продуктовый помощник».

Онлайн-сервис c API для него.

На этом сервисе пользователи могут публиковать рецепты,
подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное»,
а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

накинуто несколько тетсовых ингридиентов для удобства начинаются с t_ <ingridient>

есть нексолько тестовыз тегов (цвета тегов hex)

Собрать docker-compose:

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=

cd backend python manage.py loaddata dump.json 

sudo docker-compose up -d --build

sudo docker-compose exec backend python manage.py migrate --noinput

sudo docker-compose exec backend python manage.py collectstatic --noinput

sudo docker-compose exec backend python manage.py createsuperuser

admin@admin.com admin

В папке data файлы ingredients.json/tags.json





