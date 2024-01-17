#!/bin/bash

export FECHA=`date +%d_%m_%Y`
export NAME=farmacia_${FECHA}.dump
export DIR=/home/escudero/backup/
USER_DB=postgres
NAME_DB=farmacia
cd $DIR
> ${NAME}
export PGPASSWORD=8520+
chmod 777 ${NAME}
echo "procesando la copia de la base de datos"
pg_dump -U $USER_DB -h localhost --port 5432 -f ${NAME} $NAME_DB
echo "backup terminado"

