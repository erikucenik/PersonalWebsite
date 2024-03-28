# My Personal Website

This is the source code for my FastAPI website, where I store my articles.

# How it works

The articles I write are stored inside the `articles` folder in Markdown format.

When running `main.py`, the Markdown articles are converted into HTML content through `pandoc` and `md2article_html.py`, and the results are fit into templates (`templates`) and stored in `articles_html`, where FastAPI reads them and serves them to users.

# Requirements

- Pandoc
- requirements.txt for pip

Then just `chmod u+x gunicorn_start` and `./gunicorn_start`
