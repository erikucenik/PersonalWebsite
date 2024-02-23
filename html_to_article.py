with open("./modified.html", "r") as f:
    content = f.read()
    article = f"""
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
        {content}
	</main>

	<footer class="main__footer">
	</footer>
</body>
</html>"""

    with open("./final_article.html", "w") as fout:
        fout.write(article)
