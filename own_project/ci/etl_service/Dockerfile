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

COPY --from=requirements-stage /tmp/requirements.txt /${WORKDIR_NAME}/requirements.txt
RUN pip install --upgrade pip  \
    && pip install --no-cache-dir -r /${WORKDIR_NAME}/requirements.txt

COPY postgres_to_es/ .


ENTRYPOINT ["python", "etl_process.py"]
