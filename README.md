# My Personal Website

This is the source code for [my website](https://erikucenik.com/), where I store my articles.

# How it works

The articles I write are stored inside the `articles` folder in Markdown format.

When running `main.py`, the Markdown articles are converted into HTML content through `pandoc` and `md2article_html.py`, and the results are fit into templates (`templates`) and stored in `articles_html`, where FastAPI reads them and serves them to users.

# Requirements

- Docker
- Pandoc
- requirements.txt for pip

# Installation

```sh
docker network create traefik-public
export USERNAME=name
export PASSWORD=changethis
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

docker-compose -f docker-compose.traefik.yml up -d
docker-compose -f docker-compose.yml up -d
```

# Notes

The design files for this website can be found [here](https://github.com/erikucenik/PersonalWebsiteDesign).
