FROM python:3.11-slim


ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Requirements are installed here to ensure they will be cached.
COPY requirements/ /requirements/
RUN pip install  -r /requirements/local.txt


COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]