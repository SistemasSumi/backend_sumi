#!/bin/bash
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
echo $DJANGODIR
DJANGO_SETTINGS_MODULE=Sigban.settings.prod
cd $DJANGODIR
pwd
. env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
exec python manage.py runserver 0:8000

