FROM python:3.11-slim

LABEL org.opencontainers.image.authors="joshburnsxyz"
LABEL org.opencontainers.image.url="https://github.com/joshburnsxyz/generik"
LABEL org.opencontainers.image.source="https://github.com/joshburnsxyz/generik"
LABEL org.opencontainers.image.title="Generik"
LABEL org.opencontainers.image.description="Simple, Static service dashboard generator for Self Hosters and Home Labbers."

WORKDIR /app

RUN mkdir -p /var/www/html

COPY ./src/dashboard_generator.py /app
COPY ./src/template.html /app
COPY ./src/assets/* /var/www/html/assets

# RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8577
ENV TITLE="GENERIK DASHBOARD"
ENV THEME="solarlight"

EXPOSE 8577

ENTRYPOINT [ "python", "/app/dashboard_generator.py" ]