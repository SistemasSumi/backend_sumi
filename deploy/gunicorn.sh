#!/bin/bash

NAME="sarpsoft"
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
SOCKFILE=/tmp/gunicorn-sarpsoft.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=escudero
GROUP=escudero
NUM_WORKERS=1
TIMEOUT=600
DJANGO_WSGI_MODULE=Sigban.wsgi

rm -frv $SOCKFILE

echo $DJANGODIR

cd $DJANGODIR

exec ${DJANGODIR}/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --timeout $TIMEOUT \
  --log-level=debug \
  --log-file=$LOGDIR
