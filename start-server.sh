#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd boss-api; python manage.py createsuperuser --no-input)
fi
(cd boss-api; gunicorn mainsite.wsgi:application --bind 0.0.0.0:$PORT) &
nginx -g "daemon off;"
