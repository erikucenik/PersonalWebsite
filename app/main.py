import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from md2article_html import md2article_html
import mariadb

try:
    con = mariadb.connect(
            user="root",
            password="123",
            host="personalwebsite_mariadb_1",
            port=3306,
            database="personalwebsite"
    )
except mariadb.Error as e:
    print(f"Error connecting to Mariadb Platform: {e}")

cur = con.cursor()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name='static')

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    cur.execute("SELECT title,subtitle,endpoint FROM personalwebsite.articles ORDER BY date_published DESC")
    articles = cur.fetchall()
    articles = [{"title": title, "subtitle": subtitle, "path": endpoint} for (title, subtitle, endpoint) in articles]

    return templates.TemplateResponse(name="index.html", context={ "request": request, "articles": articles})

@app.get("/md/{article_name}", response_class=PlainTextResponse)
async def article_md(request: Request, article_name):
    with open(f"./articles/{article_name}.md", "r") as f:
        text = f.read()
        return text

@app.get("/articles/{article_name}")
async def article(request: Request, article_name):
    cur.execute(f"SELECT title,subtitle,date_published,thumbnail,endpoint FROM personalwebsite.articles WHERE endpoint='{article_name}'")
    article = cur.fetchall()

    if not article:
        return { "msg": "404 Article doesn't exist." }
    else:
        (title, subtitle, date_published, thumbnail, endpoint) = article[0]

    date_published = date_published.strftime("%d/%m/%Y")
    md_content = await article_md(request, article_name)
    html_content = md2article_html(md_content)

    return templates.TemplateResponse(name="article.html", context={ "request": request, "html_content": html_content, "title": title, "subtitle": subtitle, "thumbnail": thumbnail, "endpoint": endpoint, "date_published": date_published})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
