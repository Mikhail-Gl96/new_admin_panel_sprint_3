ARG IMAGE_NAME=python:3.10
FROM ${IMAGE_NAME} as requirements-stage
WORKDIR /tmp
COPY pyproject.toml poetry.lock /tmp/

ENV POETRY_VERSION=1.1.13

# System deps:
RUN pip install "poetry==${POETRY_VERSION}"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM ${IMAGE_NAME}

ENV WORKDIR_NAME=opt/app
RUN mkdir /${WORKDIR_NAME}

WORKDIR /${WORKDIR_NAME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY --from=requirements-stage /tmp/requirements.txt /${WORKDIR_NAME}/requirements.txt
RUN pip install --upgrade pip  \
    && pip install --no-cache-dir -r /${WORKDIR_NAME}/requirements.txt

COPY app/run_uwsgi.sh run_uwsgi.sh
COPY app/uwsgi/uwsgi.ini uwsgi.ini

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /${WORKDIR_NAME}/static/ \
     && mkdir -p /${WORKDIR_NAME}/media/

COPY app/ .

RUN python manage.py collectstatic --no-input
#RUN ./create_super_user.sh
EXPOSE 8000


ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]
