# Use official Python image (alpine-based for smaller size)
FROM python:3.9-alpine3.13

LABEL maintainer="Ndifoin Hilary"

ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

RUN apk add --no-cache \
        build-base \
        libffi-dev \
        openssl-dev \
        python3-dev \
        postgresql-dev \
        gcc \
        musl-dev \
        libgcc \
    && python -m venv /py

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false

RUN /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --no-cache --virtual .tmp-build-deps \
        build-base \
        postgresql-dev \
        musl-dev \
        zlib \
        zlib-dev && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Clean up build dependencies
RUN apk del .tmp-build-deps

# Prepare volume folders and permissions before switching user
RUN mkdir -p /vol/web/media /vol/web/static && \
    adduser -D -H django-user && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

# Set working directory and copy app
WORKDIR /app
COPY ./app /app

# Switch to non-root user
USER django-user

EXPOSE 8000

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
