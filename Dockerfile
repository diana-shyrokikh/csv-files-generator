FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE csv_gen_service.settings

WORKDIR app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

USER django-user
