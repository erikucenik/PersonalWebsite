> article_from_md.html

echo "<html>" >> article_from_md.html
pandoc article_from_erik.md -f markdown+fenced_code_blocks-auto_identifiers-smart -t html --mathjax --no-highlight >> article_from_md.html
echo "</html>" >> article_from_md.html
