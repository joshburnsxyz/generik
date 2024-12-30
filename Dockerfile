FROM python:3.11-slim

WORKDIR /app

COPY ./src/* /app
# RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8577
ENV TITLE="GENERIK DASHBOARD"
ENV THEME="solarlight"

EXPOSE 8577

CMD [ "python", "/app/dashboard_generator.py" ]