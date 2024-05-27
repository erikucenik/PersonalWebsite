# My Personal Website

This is the source code for [my website](https://erikucenik.com/), where I store my articles.

# How it works

This is a web app built using the FastAPI framework under the web server Uvicorn, it uses Traefik as a reverse proxy and everything runs inside Docker containers.

When receiving a request for an article (for example, at `https://erikucenik.com/articles/about_this`), `main.py` looks for the article's entry in the database using the endpoint of the request (`about_this`). Then it fetches its metadata and reads the article file (`app/articles/about_this.md`) and converts it to HTML using [Pandoc](https://pandoc.org/). Pandoc provides a simple conversion which isn't adapted to the design of this website (see **Notes**), so the content is again processed by `md2article_html.py`. 

# Requirements

- Docker
- Traefik
- requirements.txt for pip

# Installation

## Creating the Database

This site finds the existing articles based on their metadata, which is stored in a MariaDB database. To set up the database:

1. Establish a password for your database by editing the `MARIADB_ROOT_PASSWORD` environment variable at the `mariadb` section in `docker-compose.yml`.
2. Go through the following sections until being able to run `docker-compose -f docker-compose.yml up`.
3. Go back to this step. While the MariaDB service is running, run `docker exec -it personalwebsite_mariadb_1 mariadb -uroot -pYOUR_PASSWORD`.
4. Create a database called `personalwebsite`.
5. Run the command at `create-table.sql` to create the table containing the articles metadata.

You can access this database every time you want to create an article using the same steps.

## Setting up the articles

The articles in this website are stored in `app/articles`, so every time you want to add one, add it there in Markdown format. Then you can update the database with their metadata using commands like those in `insert-articles.sql`. There I added the ones for the existing articles.

## Traefik

This repo uses Traefik as a reverse proxy, so if you haven't already got an instance running, you will have to create one. To do this you'll first need to create a Traefik network in Docker and then add some environment variables for authentication.

```console
docker network create traefik-public
export USERNAME=name
export PASSWORD=changethis
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)

docker-compose -f docker-compose.traefik.yml up -d
```

These variables will be used for the Traefik Dashboard at `traefik.your-domain-name.com`.

## Running the site

Finally, you can `docker-compose -f docker-compose.yml up -d`.

# Notes

The design files for this website (including the database physical data model) can be found [here](https://github.com/erikucenik/PersonalWebsiteDesign).
