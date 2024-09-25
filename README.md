poetry install

./manage.py makemigrations

./manage.py migrate

./manage.py createsuperuser



For testing URLs:

bookings/                  - GET

bookings/                  - POST

bookings/<uuid:pk>/cancel/ - DELETE
