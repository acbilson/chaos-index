FROM docker.io/library/python:3.10.6-alpine3.15 as build

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# Installs python packages to the users local folder
WORKDIR /app
COPY ./src/requirements.txt /app/
RUN pip install --user -r requirements.txt

FROM docker.io/library/python:3.10.6-alpine3.15 as base
COPY --from=build /root/.local /root/.local

# (re)installs a few dependencies
RUN apk add pcre-dev git openssh

# load uwsgi config
RUN mkdir -p /etc/micropub
COPY ./template/micropub.ini /etc/micropub

# install source code
COPY ./src /app/src

#############
# Development
#############

FROM base as dev

# mount database directory here
RUN mkdir -p /mnt/db

# mount source code volume here
WORKDIR /mnt/src

ENV FLASK_ENV development
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]

############
# Production
############

FROM test as prod
WORKDIR /app/src
ENV FLASK_ENV production

ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/micropub/micropub.ini"]
