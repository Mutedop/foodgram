Foodgram

«Продуктовый помощник».
___
Онлайн-сервис c API для него.
___
На этом сервисе пользователи могут публиковать рецепты,\
подписываться на публикации других пользователей,\
добавлять понравившиеся рецепты в список «Избранное»,\
а перед походом в магазин скачивать сводный список продуктов,\
необходимых для приготовления одного или нескольких выбранных блюд.
____
Собрать docker-compose:
___
file .env |>\
DB_ENGINE=django.db.backends.postgresql\
DB_NAME=postgres\
POSTGRES_USER=postgres\
POSTGRES_PASSWORD=postgres\
DB_HOST=db\
DB_PORT=5432\
SECRET_KEY=
___
sudo docker-compose up -d --build

sudo docker-compose exec backend python manage.py migrate --noinput

sudo docker-compose exec backend python manage.py collectstatic --noinput

sudo docker-compose exec backend python manage.py loaddata fixtures/ingredients.json --app recipes/models.ingredient

sudo docker-compose exec backend python manage.py loaddata fixtures/tags.json --app recipes/models.ingredient

sudo docker-compose exec backend python manage.py createsuperuser
___
log: admin@admin.com

pass: admin
___
deploy error .
    sudo rm .env
    touch .env
    echo DB_ENGINE=${{ secrets.DB_ENGINE }} >> .env
    echo DB_NAME=${{ secrets.DB_NAME }} >> .env
    echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env
    echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env
    echo DB_HOST=${{ secrets.DB_HOST }} >> .env
    echo DB_PORT=${{ secrets.DB_PORT }} >> .env