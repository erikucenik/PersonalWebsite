import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
    cur.execute("SELECT title,subtitle,endpoint FROM personalwebsite.articles")
    articles = cur.fetchall()
    articles = [{"title": title, "subtitle": subtitle, "path": endpoint} for (title, subtitle, endpoint) in articles]

    print(articles)

    return templates.TemplateResponse(name="index.html", context={ "request": request, "articles": articles})

@app.get("/articles/{article_name}")
async def article(request: Request, article_name):
    # Buscar en la tabla la entrada que tiene como `endpoint` el valor article_name. 
    # Si no existe, devolver un error y quizás una página de 404 not found.
    # Tomar el titulo, subtitulo, contenido y fecha de creación.
    # Convertir el contenido de markdown a HTML.
    # Devolver todo.
    #cur.execute(f"SELECT title,subtitle,content,date_published FROM personalwebsite.articles WHERE endpoint={article_name}")
    #article = cur.fetchall()
    #print(article)
    return {"Hola": "Adios"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
