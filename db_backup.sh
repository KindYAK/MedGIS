#!/bin/bash -e
cd /opt/app/MedGIS
/usr/local/bin/docker-compose exec -T db chmod 777 /bin/db_backup.sh
/usr/local/bin/docker-compose exec -T db /bin/db_backup.sh
