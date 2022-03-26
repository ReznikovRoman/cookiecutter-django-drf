# Base image
FROM python:3.10

# Set default environment variables
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        git \
        gcc \
        musl-dev \
        curl \
        libc-dev \
        postgresql-client \
        postgresql-contrib \
        netcat \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements/requirements.txt requirements.txt
COPY ./requirements/requirements.dev.txt ./requirements.dev.txt
COPY ./requirements/requirements.test.txt ./requirements.test.txt
COPY ./requirements/requirements.lint.txt ./requirements.linter.txt

# Install project dependencies
RUN pip install --upgrade pip-tools
RUN pip-sync requirements.txt requirements.*.txt

# Copy entrypoint.sh
COPY entrypoint.sh .

# Copy project files
COPY . .

# Create folder for gunicorn logs
RUN mkdir -p /var/log/gunicorn

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
