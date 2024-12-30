import csv
import json
import os
import http.server
import socketserver
from pathlib import Path

# Function to read CSV and return a list of services
def read_services_from_csv(csv_file):
    services = []
    if not Path(csv_file).exists():
        print(f"No {csv_file} file found, creating a blank one at {csv_file}")
        # Create a default CSV file with sample services
        with open(csv_file, "w") as f:
            f.write("Name,URL,Category\nGithub,https://github.com,Developer\nYoutube,https://youtube.com,Media")
    
    # Read the CSV file and parse the services
    try:
        with open(csv_file, mode='r') as file:
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
                    print(f"Warning: Skipping malformed row: {row}")
        
        # If services list is empty, fill with default data
        if not services:
            print(f"Warning: The {csv_file} file is empty or malformed. Creating a default set of services.")
            with open(csv_file, "w") as f:
                f.write("Name,URL,Category\nGithub,https://github.com,Developer\nYoutube,https://youtube.com,Media")
            # Re-read after writing default content
            services = read_services_from_csv(csv_file)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        exit(1)

    return services

# Function to generate the HTML content
def generate_dashboard_html(services, page_title):
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
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 20px;  /* Adds spacing between category tiles */
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
                width: calc(33% - 20px);  /* Three categories per row */
                box-sizing: border-box;
                transition: box-shadow 0.3s ease;
                margin: 10px;
                padding: 10px;
            }}
            .category-container:hover {{
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
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
                width: 45%;  /* Two services per row inside each category */
                box-sizing: border-box;
                text-align: center;
                transition: box-shadow 0.3s ease;
            }}
            .service:hover {{
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
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
                    width: calc(50% - 20px);  /* Two categories per row on tablets */
                }}
                .service {{
                    width: 48%;  /* Two services per row inside each category */
                }}
            }}
            @media (max-width: 600px) {{
                .category-container {{
                    width: 100%;  /* One category per row on mobile */
                }}
                .service {{
                    width: 100%;  /* One service per row inside each category */
                }}
            }}
        </style>
    </head>
    <body>
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
