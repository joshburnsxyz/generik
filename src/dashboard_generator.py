import csv
import json
import os

# Function to read CSV and return a list of services
def read_services_from_csv(csv_file):
    services = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            services.append({
                'name': row['Name'],
                'url': row['URL'],
                'category': row['Category']
            })
    return services

# Function to generate the HTML content
def generate_dashboard_html(services):
    # Serialize services data to JSON format
    services_json = json.dumps(services)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Service Dashboard</title>
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
            .status {{
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background-color: grey;
                transition: background-color 0.3s ease;
            }}
            .status.up {{
                background-color: green;
            }}
            .status.down {{
                background-color: red;
            }}
            .service:hover {{
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Self-Hosted Service Dashboard</h1>
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
                <div class="status" id="status-{service['name']}"></div>
            </div>
            '''
        html_content += "</div>"  # Close category-container
    
    # Closing HTML tags
    html_content += f"""
        </div>

        <script>
            const services = {services_json};

            function checkServiceStatus() {{
                services.forEach(service => {{
                    fetch(service.url, {{ method: 'GET', mode: 'no-cors' }})
                        .then(response => {{
                            if (response.status === 200) {{
                                document.getElementById('status-' + service.name).classList.add('up');
                                document.getElementById('status-' + service.name).classList.remove('down');
                            }} else {{
                                document.getElementById('status-' + service.name).classList.add('down');
                                document.getElementById('status-' + service.name).classList.remove('up');
                            }}
                        }})
                        .catch(() => {{
                            document.getElementById('status-' + service.name).classList.add('down');
                            document.getElementById('status-' + service.name).classList.remove('up');
                        }});
                }});
            }}

            setInterval(checkServiceStatus, 5000); // Check every 5 seconds
            checkServiceStatus(); // Initial check
        </script>
    </body>
    </html>
    """
    
    return html_content

# Function to save HTML to a file
def save_html_to_file(html_content, filename="dashboard.html"):
    with open(filename, "w") as file:
        file.write(html_content)

# Main function
def main():
    csv_file = "/config/services.csv" # Mount /config as a bind directory mount from docker and create services.csv in there
    services = read_services_from_csv(csv_file)
    html_content = generate_dashboard_html(services)
    save_html_to_file(html_content)
    print("Dashboard HTML file generated successfully!")

if __name__ == "__main__":
    main()
