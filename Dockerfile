FROM python:3.10-slim

# Nastavení pracovního adresáře
WORKDIR /app

# Nastavení prostředí
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_DEBUG=0 \
    DOCKER_ENV=true

# Instalace systémových závislostí
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Kopírování requirements
COPY requirements.txt .

# Instalace Python závislostí
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování projektu
COPY . .

# Vytvoření uživatele pro běh aplikace
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Spuštění aplikace
# Přidání skriptu pro inicializaci
COPY entrypoint.sh /entrypoint.sh
USER root
RUN chmod +x /entrypoint.sh
USER appuser

# Spuštění aplikace přes entrypoint
ENTRYPOINT ["/entrypoint.sh"]
