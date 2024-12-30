import csv
import json
import os
import http.server
import socketserver
from pathlib import Path
import logging

# Global logger setup
logging.basicConfig(filename='/config/generik.log', level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CSV_CONTENT = "Name,URL,Category\nGithub,https://github.com,Developer\nYoutube,https://youtube.com,Media"

# Function to read and return services from CSV
def read_services_from_csv(csv_file):
    if not Path(csv_file).exists():
        logger.info(f"{csv_file} not found, creating with default services")
        Path(csv_file).write_text(DEFAULT_CSV_CONTENT)

    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            services = [
                {'name': row['Name'], 'url': row['URL'], 'category': row['Category']}
                for row in reader if all(k in row for k in ['Name', 'URL', 'Category'])
            ]
            if not services:
                logger.error(f"{csv_file} is empty or malformed. Writing default services.")
                Path(csv_file).write_text(DEFAULT_CSV_CONTENT)
                return read_services_from_csv(csv_file)
            return services
    except Exception as e:
        logger.error(f"Error reading {csv_file}: {e}")
        exit(1)

# Function to generate HTML content for the dashboard
def generate_dashboard_html(services, page_title, theme_class, footer_content):
    services_json = json.dumps(services)
    categories = {}

    for service in services:
        categories.setdefault(service['category'], []).append(service)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/assets/main.css" />
        <link rel="stylesheet" href="/assets/themes.css" />
        <title>{page_title}</title>
        <style>
            
        </style>
    </head>
    <body class="{theme_class}-theme">
        <div class="container">
            <h1 style="width: 100%; text-align: center;">{page_title}</h1>
    """

    for category, services_in_category in categories.items():
        html_content += f'''
        <div class="category-container">
            <div class="category-title">{category}</div>
            <div class="service-container">
        '''
        for service in services_in_category:
            html_content += f'''
            <div class="service" id="service-{service['name']}">
                <a href="{service['url']}" target="_blank">{service['name']}</a>
            </div>
            '''
        html_content += "</div></div>"

    html_content += f"""
        <footer>{footer_content}</footer>
        </div>
    </body>
    </html>
    """
    return html_content

# Function to save the HTML file
def save_html_to_file(html_content, filename="index.html"):
    output_dir = Path("/var/www/html")
    (output_dir / filename).write_text(html_content)
    logger.debug(f"HTML file saved to {output_dir / filename}")

# Function to start the HTTP server
def start_http_server(port):
    web_dir = Path('/var/www/html')
    os.chdir(web_dir)
    httpd = socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler)
    logger.info(f"Serving at http://0.0.0.0:{port}")
    httpd.serve_forever()

# Main function
def main():
    page_title = os.getenv('TITLE', 'GENERIK DASHBOARD')
    app_port = int(os.getenv('PORT', 5877))
    theme_class = os.getenv('THEME', 'light')
    footer_content = os.getenv('FOOTER', '<p>Built by <a href="https://github.com/joshburnsxyz">Josh Burns</a></p>')

    if not page_title or not app_port:
        logger.error("Error: Missing required environment variables TITLE or PORT")
        exit(1)

    csv_file = "/config/services.csv"
    services = read_services_from_csv(csv_file)
    html_content = generate_dashboard_html(services, page_title, theme_class, footer_content)
    save_html_to_file(html_content)
    start_http_server(app_port)

if __name__ == "__main__":
    main()
