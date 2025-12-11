FROM python:3.10-alpine as builder
ARG APP_VERSION=dev_build
WORKDIR /app

RUN apk update && apk add --no-cache \
    build-base \
    && rm -rf /var/cache/apk/*

COPY requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

FROM python:3.10-alpine as final
ENV APP_VERSION=$APP_VERSION
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

COPY . .

EXPOSE 5000

ENV FLASK_ENV=production
ENV SECRET_API_KEY=not_set_in_dockerfile

CMD ["python", "app.py"]
