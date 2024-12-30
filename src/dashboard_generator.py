import csv
import json
import os
import http.server
import socketserver
from pathlib import Path
import logging

# Global logger object
logging.basicConfig(filename='/config/generik.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to read CSV and return a list of services
def read_services_from_csv(csv_file):
    services = []
    if not Path(csv_file).exists():
        logger.info(f"No {csv_file} file found, creating a blank one at {csv_file}")
        # Create a default CSV file with sample services
        with open(csv_file, "w") as f:
            f.write("Name,URL,Category\nGithub,https://github.com,Developer\nYoutube,https://youtube.com,Media")
    
    # Read the CSV file and parse the services
    try:
        with open(csv_file, mode='r') as file:
            logger.info(f"{csv_file} file found")
            reader = csv.DictReader(file)
            for row in reader:
                # Check that necessary columns exist
                if 'Name' in row and 'URL' in row and 'Category' in row:
                    services.append({
                        'name': row['Name'],
                        'url': row['URL'],
                        'category': row['Category']
                    })
                else:
                    logger.info(f"Skipping malformed row: {row}")
        
        # If services list is empty, fill with default data
        if not services:
            logger.error(f"Warning: The {csv_file} file is empty or malformed. Creating a default set of services.")
            with open(csv_file, "w") as f:
                f.write("Name,URL,Category\nGithub,https://github.com,Developer\nYoutube,https://youtube.com,Media")
            # Re-read after writing default content
            services = read_services_from_csv(csv_file)
    except Exception as e:
        logger.error(f"Error reading {csv_file}: {e}")
        exit(1)

    return services

# Function to generate the HTML content
def generate_dashboard_html(services, page_title, theme_class, foooter_content):
    services_json = json.dumps(services)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en" >
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_title}</title>
        <style>
/* Default Theme (Light Theme) */
body {{
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #333;
    margin: 0;
    padding: 0;
}}

/* Dark Theme */
body.dark-theme {{
    background-color: #333;
    color: #fff;
}}

body.dark-theme .container {{
    background-color: #444;
}}

body.dark-theme .category-container {{
    background-color: #555;
    color: #ddd;
}}

/* Blue Theme */
body.blue-theme {{
    background-color: #f0f8ff;
    color: #1e3a56;
}}

body.blue-theme .container {{
    background-color: #e6f0fa;
}}

body.blue-theme .category-container {{
    background-color: #cce0ff;
    color: #1e3a56;
}}

/* Solarlight Theme */
body.solarlight-theme {{
    background-color: #fdf6e3;
    color: #657b83;
}}

body.solarlight-theme .container {{
    background-color: #fdf6e3;
    color: #657b83;
}}

body.solarlight-theme .category-container {{
    background-color: #eee8d5;
    color: #586e75;
}}

body.solarlight-theme .category-title {{
    background-color: #93a1a1;
    color: #fdf6e3;
}}

body.solarlight-theme .service {{
    background-color: #fdf6e3;
    color: #657b83;
    border: 1px solid #93a1a1;
}}

body.solarlight-theme .service a {{
    color: #268bd2;
}}

body.solarlight-theme .service a:hover {{
    color: #268bd2;
}}

/* Hover effects for category containers and services */
body.solarlight-theme .category-container:hover {{
    background-color: #dce0e0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}}

body.solarlight-theme .service:hover {{
    background-color: #eee8d5;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}}

/* Solardark Theme */
body.solardark-theme {{
    background-color: #002b36;
    color: #93a1a1;
}}

body.solardark-theme .container {{
    background-color: #002b36;
    color: #93a1a1;
}}

body.solardark-theme .category-container {{
    background-color: #073642;
    color: #93a1a1;
}}

body.solardark-theme .category-title {{
    background-color: #586e75;
    color: #fdf6e3;
}}

body.solardark-theme .service {{
    background-color: #073642;
    color: #93a1a1;
    border: 1px solid #586e75;
}}

body.solardark-theme .service a {{
    color: #268bd2;
}}

body.solardark-theme .service a:hover {{
    color: #268bd2;
}}

/* Hover effects for category containers and services */
body.solardark-theme .category-container:hover {{
    background-color: #2a3c3a;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}}

body.solardark-theme .service:hover {{
    background-color: #586e75;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}}


/* General styling for the tiles */
.container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}}

.category-container {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: stretch;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    width: calc(33% - 20px);
    box-sizing: border-box;
    transition: box-shadow 0.3s ease;
    margin: 10px;
    padding: 10px;
}}

.category-title {{
    font-size: 1.5em;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
    text-align: center;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
}}

.service-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}}

.service {{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    width: 45%;
    box-sizing: border-box;
    text-align: center;
    transition: box-shadow 0.3s ease;
}}

.service a {{
    text-decoration: none;
    color: #333;
    font-size: 1.1em;
    font-weight: bold;
    display: block;
}}

.service a:hover {{
    color: #007BFF;
}}

@media (max-width: 1024px) {{
    .category-container {{
        width: calc(50% - 20px);
    }}
    .service {{
        width: 48%;
    }}
}}

@media (max-width: 600px) {{
    .category-container {{
        width: 100%;
    }}
    .service {{
        width: 100%;
    }}
}}

        </style>
    </head>
    <body class="{theme_class}-theme">
        <div class="container">
            <h1 style="width: 100%; text-align: center;">{page_title}</h1>
    """

    # Group services by category
    categories = {}
    for service in services:
        category = service['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(service)

    # Create category containers with service tiles inside each category
    for category, services_in_category in categories.items():
        html_content += f'''
        <div class="category-container">
            <div class="category-title">{category}</div>
            <div class="service-container">
        '''
        
        # Add each service as a tile inside the category container
        for service in services_in_category:
            html_content += f'''
            <div class="service" id="service-{service['name']}">
                <a href="{service['url']}" target="_blank">{service['name']}</a>
            </div>
            '''
        
        # Closing tags for category container
        html_content += "</div></div>"

    # Closing HTML tags
    html_content += f"""
        <footer>{footer_content}</footer>
        </div>
    </body>
    </html>
    """
    
    return html_content

# Function to save HTML to a file
def save_html_to_file(html_content, filename="index.html"):
    output_dir = Path("/var/www/html")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    with open(output_file, "w") as file:
        file.write(html_content)
    logger.debug(f"HTML file saved to {output_file}")

# Function to start the HTTP server
def start_http_server(port):
    os.chdir("/var/www/html")  # Set the working directory to where the HTML file is saved
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    logger.info(f"Serving at http://localhost:{port}")
    httpd.serve_forever()

# Main function
def main():
    # Pull in settings from environment
    page_title = os.getenv('TITLE', 'GENERIK DASHBOARD')  # Default title if not set
    app_port = int(os.getenv('PORT', 5877))  # Default port if not set
    selected_theme = os.getenv('THEME', 'light_theme')  # Default theme if not set
    selected_theme = os.getenv('FOOTER', '<p>Built by <a href="https://github.com/joshburnsxyz">Josh Burns</a></p>, Provided under the MIT Open-Source License.')  # Default footer content

    if not page_title:
        logger.error("Error: Missing required environment variable TITLE")
        exit(1)
    if not app_port:
        logger.error("Error: Missing required environment variable PORT")
        exit(1)

    csv_file = "/config/services.csv"  # Mount /config as a bind directory from Docker and create services.csv in there
    services = read_services_from_csv(csv_file)
    html_content = generate_dashboard_html(services, page_title, selected_theme, footer_content)
    save_html_to_file(html_content)
    start_http_server(app_port)  # Start the HTTP server on the port defined by environment variable

if __name__ == "__main__":
    main()
