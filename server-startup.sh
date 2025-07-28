#!/bin/bash
set -e

docker-compose run --rm web python manage.py test

docker-compose up --build