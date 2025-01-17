FROM python:3.9-bullseye

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    libssl-dev \
    libreoffice \
    libreoffice-writer \
    python3-uno \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8007
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8007"]
