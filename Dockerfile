FROM python:3.10.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY r.txt /code/
RUN pip install -r r.txt
COPY . /code/