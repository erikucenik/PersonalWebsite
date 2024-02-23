import subprocess
from xml.dom import minidom

def convert_iframes(domtree):
    links = domtree.getElementsByTagName("a")
    
    for link in links:
        paragraph = link.parentNode
        text = link.firstChild 

        if not link.firstChild.nodeType:
            continue
        if text.nodeType != link.TEXT_NODE:
            continue

        if text.nodeValue == "iframe":
            address = link.getAttribute("href")
            iframe = domtree.createElement("iframe")
            iframe.appendChild(domtree.createTextNode(""))
            iframe.setAttribute("width", "560")
            iframe.setAttribute("height", "315")
            iframe.setAttribute("src", address)
            iframe.setAttribute("title", "YouTube video player")
            iframe.setAttribute("frameborder", "0")
            iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share")
            iframe.setAttribute("allowfullscreen", "")
            iframe.setAttribute("class", "article__iframe")
            domtree.firstChild.insertBefore(iframe, paragraph)
            domtree.firstChild.removeChild(paragraph)

def convert_downloads(domtree):
    links = domtree.getElementsByTagName("a")
    
    for link in links:
        paragraph = link.parentNode
        text = link.firstChild 

        if not link.firstChild.nodeType:
            continue
        if text.nodeType != link.TEXT_NODE:
            continue

        if text.nodeValue == "download":
            download_section = domtree.createElement("section")
            download_section.setAttribute("class", "download")

            download_img = domtree.createElement("img")
            download_img.setAttribute("class", "download__icon")
            download_img.setAttribute("src", "media/cloud.png")
            download_section.appendChild(download_img)

            filename = link.getAttribute("href").split("/")[-1]
            download_p = domtree.createElement("p")
            download_p.setAttribute("class", "download__filename")
            download_p.appendChild(domtree.createTextNode(filename))
            download_section.appendChild(download_p)

            download_a = domtree.createElement("a")
            download_a.setAttribute("href", "media/cloud.png")
            download_a.setAttribute("class", "download__square")
            download_a.setAttribute("download", "")
            download_icon = domtree.createElement("img")
            download_icon.setAttribute("class", "download__icon")
            download_icon.setAttribute("src", "media/download.png")
            download_a.appendChild(download_icon)
            download_section.appendChild(download_a)

            domtree.firstChild.insertBefore(download_section, paragraph)
            domtree.firstChild.removeChild(paragraph)

def convert_codelines(domtree):
    code_elements = domtree.getElementsByTagName("code")

    for code_element in code_elements:
        if code_element.parentNode.tagName != "pre":
            code_element.setAttribute("class", "article__code")

def convert_codeblocks(domtree):
    code_elements = domtree.getElementsByTagName("code")

    for code_element in code_elements:
        if code_element.parentNode.tagName == "pre":
            create_code_block(domtree, code_element)

def convert_headers(domtree):
    headers = domtree.getElementsByTagName("h1")
    for h1 in headers:
        h1.setAttribute("class", "article__header")
    
    subheaders = []
    for i in range(2, 7):
        subheaders += domtree.getElementsByTagName(f"h{i}")
        
        for hn in subheaders:
            hn.setAttribute("class", "article__subheader")

def convert_figures(domtree):
    figures = domtree.getElementsByTagName("figure")
    for figure in figures:
        figure.setAttribute("class", "figure")
        children = figure.childNodes
        
        for child in children:
            if child.nodeType == child.TEXT_NODE:
                continue
            if child.tagName == "img":
                child.setAttribute("class", "figure__image")
            if child.tagName == "figcaption":
                child.setAttribute("class", "figure__caption")

def strong2b(domtree):
    strongs = domtree.getElementsByTagName("em")
    for strong in strongs:
        strong.tagName = "b"

def em2i(domtree):
    italics = domtree.getElementsByTagName("em")
    for em in italics:
        em.tagName = "i"

def add_styling_class_to_elements(domtree, tagname):
    elements = domtree.getElementsByTagName(tagname)
    for element in elements:
        element.setAttribute("class", f"article__{tagname}")

def create_code_block(domtree, code_element):
    pre_element = code_element.parentNode
    language = pre_element.getAttribute("class")

    pre_element.setAttribute("class", "codeblock-window__pre")
    code_element.setAttribute("class", f"codeblock-window__code language-{language}")

    codeblock_window = domtree.createElement("section")
    codeblock_window.setAttribute("class", "codeblock-window")
    domtree.firstChild.insertBefore(codeblock_window, pre_element)

    codeblock_window_bar = domtree.createElement("section")
    codeblock_window_bar.setAttribute("class", "codeblock-window__bar")

    codeblock_window_buttons = domtree.createElement("img")
    codeblock_window_buttons.setAttribute("class", "codeblock-window__buttons")
    codeblock_window_buttons.setAttribute("src", "media/window_buttons.png")

    [filename, code] = code_element.firstChild.toxml().split('\n', 1)
    code_element.firstChild.replaceWholeText(code)
    filename_node = domtree.createTextNode(filename)
    codeblock_window_name = domtree.createElement("p")
    codeblock_window_name.setAttribute("class", "codeblock-window__name")
    codeblock_window_name.appendChild(filename_node)
    codeblock_window_bar.appendChild(codeblock_window_buttons)
    codeblock_window_bar.appendChild(codeblock_window_name)

    codeblock_window_codespace = domtree.createElement("section")
    codeblock_window_codespace.setAttribute("class", "codeblock-window__codespace")
    codeblock_window_codespace.appendChild(pre_element)

    codeblock_window.appendChild(codeblock_window_bar)
    codeblock_window.appendChild(codeblock_window_codespace)

def pandoc_format_to_my_style(pandoc_output):
    domtree = minidom.parseString(pandoc_output)

    for tagname in ["p", "ul", "ol", "li", "a"]:
        add_styling_class_to_elements(domtree, tagname)

    em2i(domtree)
    strong2b(domtree)
    convert_headers(domtree)
    convert_figures(domtree)
    convert_codeblocks(domtree)
    convert_codelines(domtree)
    convert_iframes(domtree)
    convert_downloads(domtree)

    # Hack to remove the html and XML tags.
    my_style_html = domtree.childNodes[0].toprettyxml(newl='\n')
    my_style_html = my_style_html[:my_style_html.rfind('\n')]
    my_style_html = my_style_html[:my_style_html.rfind('\n')]
    my_style_html = my_style_html.split('\n', 1)[1]

    return my_style_html


def main(filename):
    pandoc_output = "<html>\n" +  subprocess.run(["pandoc", filename, "-f", "markdown+fenced_code_blocks-auto_identifiers-smart", "-t", "html", "--mathjax", "--no-highlight"], stdout=subprocess.PIPE).stdout.decode("utf-8") + "\n</html>"
    article_content = pandoc_format_to_my_style(pandoc_output)

    article_html = f"""
<html>
<head>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
	<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">

	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/xcode.min.css">
	<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
	<!-- and it's easy to individually load additional languages -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script>
	<script>hljs.highlightAll();</script>

	<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
	<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

	<link rel="stylesheet" type="text/css" href="article.css">
	<script src="article.js" defer></script>
</head>

<body>
	<main class="main">
		<a class="main__colorscheme-button" href="index.html"><img src="media/home.png"/></a>
		<h1 class="main__title">TITULO</h1>
        {article_content}
	</main>

	<footer class="main__footer">
	</footer>
</body>
</html>"""
    
    filename_with_html_extension = filename.split(".")[0] + ".html"

    with open(filename_with_html_extension, "w") as f:
        f.write(article_html)

if __name__ == "__main__":
    main("article.md")
