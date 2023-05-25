#!/bin/sh

cp ~/vit/winter2022/latex-templates/project-template.tex $1.tex

nvim $1.tex "+normal 9G3|"
