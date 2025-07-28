#!/bin/bash

echo "Stopping and removing all containers for the booking service..."

docker-compose down
# Если нужно удалять и данные тоже, то
# docker-compose down -v

echo "All containers have been stopped and removed."
