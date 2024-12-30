import csv
import json
import os
import http.server
import socketserver
from pathlib import Path

# Function to read CSV and return a list of services
def read_services_from_csv(csv_file):
    services = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                services.append({
                    'name': row['Name'],
                    'url': row['URL'],
                    'category': row['Category']
                })
        if not services:
            raise ValueError("CSV file is empty")
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' was not found.")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    return services

# Function to generate the HTML content
def generate_dashboard_html(services, page_title):
    # Serialize services data to JSON format
    services_json = json.dumps(services)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .category-container {{
                margin-bottom: 40px;
                border: 2px solid #ddd;
                border-radius: 10px;
                background-color: #fff;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                padding: 15px;
            }}
            .category {{
                font-size: 1.6em;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
                text-transform: uppercase;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }}
            .service {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #fff;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .service a {{
                text-decoration: none;
                color: #333;
                font-size: 1.1em;
            }}
            .service:hover {{
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{page_title}</h1>
    """
    
    # Group services by category
    categories = {}
    for service in services:
        category = service['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(service)
    
    # Add services to HTML content, grouped by categories
    for category, services_in_category in categories.items():
        html_content += f'''
        <div class="category-container">
            <div class="category">{category}</div>
        '''
        for service in services_in_category:
            html_content += f'''
            <div class="service" id="service-{service['name']}">
                <a href="{service['url']}" target="_blank">{service['name']}</a>
            </div>
            '''
        html_content += "</div>"  # Close category-container
    
    # Closing HTML tags
    html_content += f"""
        </div>
    </body>
    </html>
    """
    
    return html_content

# Function to save HTML to a file
def save_html_to_file(html_content, filename="dashboard.html"):
    output_dir = Path("/var/www/html")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename
    with open(output_file, "w") as file:
        file.write(html_content)
    print(f"HTML file saved to {output_file}")

# Function to start the HTTP server
def start_http_server(port):
    os.chdir("/var/www/html")  # Set the working directory to where the HTML file is saved
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print(f"Serving at http://localhost:{port}")
    httpd.serve_forever()

# Main function
def main():
    # Pull in settings from environment
    page_title = os.getenv('TITLE', 'GENERIK DASHBOARD')  # Default title if not set
    app_port = int(os.getenv('PORT', 5877))  # Default port if not set

    if not page_title:
        print("Error: Missing required environment variable TITLE")
        exit(1)
    if not app_port:
        print("Error: Missing required environment variable PORT")
        exit(1)

    csv_file = "/config/services.csv"  # Mount /config as a bind directory from Docker and create services.csv in there
    services = read_services_from_csv(csv_file)
    html_content = generate_dashboard_html(services, page_title)
    save_html_to_file(html_content)
    start_http_server(app_port)  # Start the HTTP server on the port defined by environment variable

if __name__ == "__main__":
    main()
