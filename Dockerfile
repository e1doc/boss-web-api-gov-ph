# Dockerfile

FROM python:3.8-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN apt-get install build-essential
RUN apt-get install libgirepository1.0-dev vim -y
# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/boss-api
COPY requirements.txt start-server.sh /opt/app/
RUN true
COPY .pip_cache /opt/app/pip_cache/
RUN true
COPY . /opt/app/boss-api/
RUN mkdir -p /opt/app/boss-api/mainsite/static
RUN true
WORKDIR /opt/app
ADD ./.profile.d /app/.profile.d
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN pip install --upgrade pip
RUN pip --version
RUN pip3 install pep517
RUN pip3 install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN pip3 install django-sequences
RUN chown -R www-data:www-data /opt/app

# collect static files
RUN cd boss-api; python manage.py collectstatic --noinput

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]