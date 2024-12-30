FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /var/www/html

COPY ./src/dashboard_generator.py /app
COPY ./src/themes.css /var/www/html

# RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8577
ENV TITLE="GENERIK DASHBOARD"
ENV THEME="solarlight"

EXPOSE 8577

CMD [ "python", "/app/dashboard_generator.py" ]