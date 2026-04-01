FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PORT=8000
ENV VC_APP_ENV=production
ENV VC_DEBUG=false
ENV VC_MEDIA_ROOT=/data/media

WORKDIR /app

RUN useradd --create-home appuser \
    && mkdir -p /data/media

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
