FROM python:3.11-slim

WORKDIR /app

COPY ./src/* /app
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8577

# Run the Python script when the container starts to generate the dashboard
RUN python dashboard_generator.py

# TODO: Boot up small webserver to serve the static web page
# CMD server /html/index.html
