# Generik Dashboard

Simple static dashboard for self-hosters 

![Docker Pulls](https://img.shields.io/docker/pulls/joshburnsxyz/generik)


## Features
- **Dynamic Dashboard**: Renders services grouped by category in a clean, user-friendly interface.
- **Themes**: Supports different themes including Light, Dark, Blue, and Solarized (light and dark) inspired themes.
- **Built for Docker**: Can be deployed using Docker for easy setup.
- **Responsive**: Optimized for desktop and mobile screens.

## Usage

All the services are defined in a CSV file that is mounted to the cotainer at `/config/services.csv`.

```csv
Name,URL,Category
Github,https://github.com,Developer
Youtube,https://youtube.com,Media
```

Each `Category` will become a box on the screen, and each service tagged with that category will become a tile inside of that box. (Screenshots to come).

## Installation

### Docker

```shell
docker run \
    -p 5877:5877 \
    -v /path/to/config:/config \
    -e THEME="solardark" \ # Set theme (light,dark,blue,solarlight,solardark are all accepted values) (optional)
    -e PORT="5877" \ # Set port the server will run on (must also reflect the forward port) (optional)
    -e TITLE="My Dashboard" \ # Set the page title and heading (optional)
    -e FOOTER="<p>Some HTML here</p>" \ # Set the HTML for the page footer (optional)
    -e ICONS="dashboard" \ # Set the icon theme to use (dashboard,fontawesome,none are all accepted values) (optional)
    joshburnsxyz/generik:latest
```

### Docker Compose

```yaml
services:
  generik-dashboard:
    image: joshburnsxyz/generik:latest
    ports:
      - "5877:5877"
    volumes:
      - /path/to/config:/config
    environment:
      TITLE: "My Custom Dashboard"
      PORT: 5877
      THEME: "solarlight"
      FOOTER: "<p>Powered by <a href='https://github.com/joshburnsxyz/generik'>Generik Dash</a></p>"
      ICONS: "dashboard"
```

```console
docker compose up
```