# ---- Base image ----
FROM python:3.12-slim

# ---- Runtime env ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- Install deps (cache-friendly) ----
# Kopiera in requirements först för bättre layer-cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app ----
# Kopiera in all kod (inkl. templates/static)
COPY . /app

# ---- Non-root user (bättre säkerhet) ----
RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

# ---- Expose port ----
EXPOSE 8000

# ---- Start command ----
# wsgi:app pekar på din wsgi.py (från föregående steg)
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "60"]
