# Use official Python image (alpine-based for smaller size)
FROM python:3.9-alpine3.13

LABEL maintainer="Ndifoin Hilary"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# Install OS-level deps and create a virtualenv
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

# Install Python deps early to benefit from Docker layer caching
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
ARG DEV=false
RUN /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update-no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps


# Add unprivileged user for security
RUN adduser -D -H django-user

# Set working directory and copy app code
WORKDIR /app
COPY ./app /app

# Switch to non-root user
USER django-user

# Expose the port your app runs on
EXPOSE 8000

# Default command (override this in Docker Compose or ECS task definition)
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
