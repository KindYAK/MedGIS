#!/usr/bin/env bash
set -e
cd web
docker build . -f docker/Dockerfile -t web

cd ..
cd airflow-worker
docker build . -f Dockerfile -t airflow-worker
