import csv
import json
import os
import http.server
import socketserver
from pathlib import Path
import logging
import signal
import sys

# Global logger setup
logger = logging.getLogger(__name__)

# Define log format
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# Create a console handler to log to STDOUT (console)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # Set to DEBUG level to capture all logs
console_handler.setFormatter(logging.Formatter(log_format))

# Create a file handler to log to a file
file_handler = logging.FileHandler('/config/generik.log')
file_handler.setLevel(logging.DEBUG)  # Set to DEBUG level to capture all logs
file_handler.setFormatter(logging.Formatter(log_format))

# Add both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Set global logging level
logger.setLevel(logging.DEBUG)


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

# Function to generate HTML content for the dashboard by replacing placeholders in the template
def generate_dashboard_html(services, page_title, theme_class, footer_content):
    services_json = json.dumps(services)
    categories = {}

    for service in services:
        categories.setdefault(service['category'], []).append(service)

    # Load the external HTML template
    template_path = Path('/app/template.html')
    if not template_path.exists():
        logger.error("HTML template file 'template.html' not found!")
        exit(1)

    with open(template_path, 'r') as template_file:
        html_template = template_file.read()

    # Generate the categories and services HTML content
    category_html = ""
    for category, services_in_category in categories.items():
        category_html += f'''
        <div class="category-container">
            <div class="category-title">{category}</div>
            <div class="service-container">
        '''
        for service in services_in_category:
            category_html += f'''
            <div class="service" id="service-{service['name']}">
                <a href="{service['url']}" target="_blank">{service['name']}</a>
            </div>
            '''
        category_html += "</div></div>"

    # Replace placeholders in the template with actual content
    html_content = html_template.replace("{{page_title}}", page_title)
    html_content = html_content.replace("{{theme_class}}", theme_class)
    html_content = html_content.replace("{{category_html}}", category_html)
    html_content = html_content.replace("{{footer_content}}", footer_content)

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
    signal.signal(signal.SIGINT, shutdown_server)

def shutdown_server(signal, frame):
    logger.info("Shutting down the server.")
    sys.exit(0)

# Main function
def main():
    page_title = os.getenv('TITLE', 'GENERIK DASHBOARD')
    app_port = int(os.getenv('PORT', 5877))
    theme_class = os.getenv('THEME', 'light')
    footer_content = os.getenv('FOOTER', '<p>Built by <a href="https://github.com/joshburnsxyz">Josh Burns</a></p>')

    if not page_title:
        logger.error("Error: Missing required environment variable TITLE")
        exit(1)    
    if not app_port:
        logger.error("Error: Missing required environment variable PORT")
        exit(1)

    csv_file = "/config/services.csv"
    services = read_services_from_csv(csv_file)
    html_content = generate_dashboard_html(services, page_title, theme_class, footer_content)
    save_html_to_file(html_content)
    start_http_server(app_port)

if __name__ == "__main__":
    main()