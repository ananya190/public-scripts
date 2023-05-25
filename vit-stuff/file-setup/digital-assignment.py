#!/bin/sh
#
# copy file to working directory and open at line and column
cp ~/vit/winter2022/latex-templates/da-template.tex $1.tex

nvim $1.tex "+normal 5G25|"
