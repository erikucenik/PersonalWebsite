import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from md2article_html import md2article_html

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name='static')
templates = Jinja2Templates(directory="templates")

articles_filenames = [filename for filename in os.listdir("articles")]
articles_filepaths = [os.path.join("articles", filename) for filename in os.listdir("articles")]

def get_article_title_subtitle_and_path(filename, filepath):
    with open(filepath, "r") as f:
        content = f.read()
        header = content.split("\n", 4)
        article_title = header[1].split(":", 1)[1].strip()
        article_subtitle = header[2].split(":", 1)[1].strip()
        article_path = filename.rsplit(".", 1)[0]

        return (article_title, article_subtitle, article_path)

if not os.path.exists("articles_html"):
    os.mkdir("articles_html")

for (filename, filepath) in zip(articles_filenames, articles_filepaths):
    (title, subtitle, path) = get_article_title_subtitle_and_path(filename, filepath)
    (article_title, article_subtitle, article_path) = get_article_title_subtitle_and_path(filename, filepath)

    article_html = md2article_html(filepath)
    article_html = f'<h1 class="main__title">{title}</h1>' + article_html

    filename_html = path + ".html"
    with open(f"articles_html/{filename_html}", "w") as fout:
        fout.write(article_html)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    articles_filenames = [filename for filename in os.listdir("articles")]
    articles_filepaths = [os.path.join("articles", filename) for filename in os.listdir("articles")]

    articles = []

    for (filename, filepath) in zip(articles_filenames, articles_filepaths):
        with open(filepath, "r") as f:
            content = f.read()
            header = content.split("\n", 4)
            article_title = header[1].split(":", 1)[1][1:]
            article_subtitle = header[2].split(":", 1)[1][1:]
            article_path = filename.rsplit(".", 1)[0]
            
            article = {"path": article_path, "title": article_title, "subtitle": article_subtitle}
            articles.append(article)

    return templates.TemplateResponse(request=request, name="index.html", context={ "articles": articles })

@app.get("/articles/{article_name}")
async def article(request: Request, article_name):
    (title, _, _) = get_article_title_subtitle_and_path(article_name + ".md", "articles/" + article_name + ".md")

    with open(f"articles_html/{article_name}.html", "r") as f:
        content = f.read()
        return templates.TemplateResponse(request=request, name="article.html", context={ "html_content": content, "article_title": title })

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./static/favicon.ico")
