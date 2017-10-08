#!/bin/bash

set -e
cmd="$@"

until python /app/fusebox/manage.py migrate; do
  echo "Migrations failed"
done

python /app/fusebox/manage.py createsuperuser --noinput --username "admin" --email "tito@pixelfusion.co.nz" || true

gunicorn -b $cmd