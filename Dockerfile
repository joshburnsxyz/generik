FROM python:3.11-slim

LABEL org.opencontainers.image.authors="joshburnsxyz"
LABEL org.opencontainers.image.url="https://github.com/joshburnsxyz/generik"
LABEL org.opencontainers.image.source="https://github.com/joshburnsxyz/generik"
LABEL org.opencontainers.image.title="Generik"
LABEL org.opencontainers.image.version="0.1.3"
LABEL org.opencontainers.image.description="Simple, Static service dashboard generator for Self Hosters and Home Labbers."

WORKDIR /app

RUN mkdir -p /var/www/html

COPY ./src/dashboard_generator.py /app
COPY ./src/template.html /app
COPY ./src/assets /var/www/html/assets

# RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8577
ENV TITLE="GENERIK DASHBOARD"
ENV THEME="solarlight"
ENV ICONS="dashboard"

EXPOSE $PORT

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:$PORT || exit 1

ENTRYPOINT [ "python", "/app/dashboard_generator.py" ]