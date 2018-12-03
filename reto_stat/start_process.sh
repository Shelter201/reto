#!/bin/bash

sleep 30
python manage.py migrate
nohup python manage.py addpoll &
nohup python manage.py updatestats &
python manage.py runserver 0.0.0.0:8000
