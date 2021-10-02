# praktikum_new_diplom

- перебить текст валиков на нормальный

Проект запустится на адресе http://localhost

API вы сможете по адресу http://localhost/api/docs/

- косяки на запросах апи
- картинку отдельной базой на фаил
- раскидать ооп классов рецептов
- админка
- чек вербосы
- первым отправить код на Ревью, датасерв не собирать



sudo docker-compose exec backend python manage.py migrate --noinput
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input

sudo docker-compose exec -it backend bash python manage.py dumpdata > ingredients.json
sudo docker-compose exec backend python manage.py loaddata ingredients.json
sudo docker-compose exec backend python manage.py loaddata tags.json