FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cron \
    libgl1 \
    libglib2.0-0 \
    libpq-dev \
    wget \
    ca-certificates \
    gnupg \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install --prefer-binary -r requirements.txt

COPY cronjob /etc/cron.d/inference-cron
RUN chmod 0644 /etc/cron.d/inference-cron \
 && crontab /etc/cron.d/inference-cron

COPY . .

CMD ["cron", "-f"]
