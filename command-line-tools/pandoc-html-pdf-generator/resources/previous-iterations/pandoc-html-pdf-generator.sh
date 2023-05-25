#!/bin/sh
# pandoc note generation

file=$1

filename=$(basename $1 .md)


`pandoc -f markdown -t pdf "$file" -o "$filename.pdf" --toc --listings --filter pandoc-xnos` && echo "converted to pdf"
`pandoc -f markdown -t html "$file" -o "$filename.html" -s --mathjax --toc --listings --filter pandoc-xnos` && echo "converted to html"