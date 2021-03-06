## [Foodgram](62.84.122.28)

«Продуктовый помощник».

![example workflow](https://github.com/mutedop/foodgram-project-react/actions/workflows/main.yml/badge.svg)

___
Онлайн-сервис c API для него.
___
На этом сервисе пользователи могут публиковать рецепты,\
подписываться на публикации других пользователей,\
добавлять понравившиеся рецепты в список «Избранное»,\
а перед походом в магазин скачивать сводный список продуктов,\
необходимых для приготовления одного или нескольких выбранных блюд.
___
___
![/](.github/forgit/home_page.png)
___
#### Для запуска
- Склонировать репозиторий
    >[foodgram](https://github.com/Mutedop/foodgram-project-react)

- Запустить свой ssh сервер

- Установим docker на cервер 
    >sudo apt install docker.io

- Установим docker-compose на сервер
    >[docker-compose](https://docs.docker.com/compose/install/)

- Файлы docker-compose.yml и nginx.conf скопировать из проект (директория infra)
на сервер

    >scp docker-compose.yml username@host:/home/username/docker-compose.yml\
    scp nginx.conf          username@host:/home/username/nginx.conf

- Фаил .env для deploy в workflows

    >touch .env\
    echo DB_ENGINE=${{ secrets.DB_ENGINE }} >> .env\
    echo DB_NAME=${{ secrets.DB_NAME }} >> .env\
    echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env\
    echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env\
    echo DB_HOST=${{ secrets.DB_HOST }} >> .env\
    echo DB_PORT=${{ secrets.DB_PORT }} >> .env

- на сервере .env можно размесить самому в корневой директории

    >Пример:\
    DB_ENGINE=django.db.backends.postgresql\
    DB_NAME=postgres\
    POSTGRES_USER=postgres\
    POSTGRES_PASSWORD=postgres\
    DB_HOST=db\
    DB_PORT=5432\
    SECRET_KEY="django-insecure-@56xgy...."

- Все secrets на [GitHub](https://github.com/)
    > project/settings/secrets/actions

___
Собрать docker-compose:

___
    sudo docker-compose up -d --build
    
    sudo docker-compose exec backend python manage.py migrate --noinput
    
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    
    sudo docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
    
    sudo docker-compose exec backend python manage.py createsuperuser
___
> Образы [DockerHub](https://hub.docker.com/repositories)

https://hub.docker.com/repository/docker/mutedop/foodgram_backend

https://hub.docker.com/repository/docker/mutedop/foodgram_frontend
___
#### FOR MORE
___

![admin](.github/forgit/admin_panel.png)
![create](.github/forgit/create_recipe.png)
![ingredients](.github/forgit/ingredients.png)
![recipe](.github/forgit/recipe.png)
![register](.github/forgit/register.png)
