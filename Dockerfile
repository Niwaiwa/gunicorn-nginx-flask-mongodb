FROM python:3.6-slim

ARG PROJECT_ENV=test

ENV PROJECT_ENV=${PROJECT_ENV} \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.1.12

RUN cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime \
    && echo "Asia/Taipei" > /etc/timezone

RUN apt-get update && apt-get install -y build-essential python-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install $(test "$PROJECT_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# performance up for future
# RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
# RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

ADD ./app /app

CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:8000", "app:app"]

