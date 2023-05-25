#!/bin/sh
# pandoc note generation

# set array to hold all files passed in argument
arguments=("$@")

# if an argument is "-of", the next argument is the output format
# if an argument is "-bf", the next argument is the bibliography file and the next argument is the bibliography style

# setting the options
output_format=""
bibliography_file=""
bibliography_style=""
citation_style=""

# find options
i=0
while [[ $i -lt ${#arguments[@]} ]]; do
    if [[ ${arguments[$i]} == "-of" ]]; then
        # set the output format to the argument, then remove both the option and the argument
        output_format=${arguments[$i+1]}
        unset arguments[$i]
        unset arguments[$i+1]
        # increment i by 2 to skip the next argument
        i=$((i+2))
    elif [[ ${arguments[$i]} == "-bf" ]]; then
        bibliography_file=${arguments[$i+1]}
        bibliography_style=${arguments[$i+2]}
        unset arguments[$i]
        unset arguments[$i+1]
        unset arguments[$i+2]
        i=$((i+3))
    elif [[ ${arguments[$i]} == "-cf" ]]; then
        citation_style=${arguments[$i+1]}
        unset arguments[$i]
        unset arguments[$i+1]
        i=$((i+2))
    else
        i=$((i+1))
    fi
done
echo "output format: $output_format"
# if no output formats are given, add html, pdf and bibliography to the output formats.
if [[ $output_format == "" ]]; then
    output_format="hpb"
fi

# if only bibliography is given, add html and pdf to the output formats.
if [[ $output_formats == "b" ]]; then
    output_format="hpb"
fi

echo "output formats: $output_format"

# # if no listings file is given, use the default
# if [[ $listings_file == "" ]]; then
#     listings_file=/Users/ananyageorge/.scripts/command-line-tools/pandoc-html-pdf-generator-resources/listings-setup.txt
# fi

# echo "listings file: $listings_file"

# if no bibliography file is given, use the default
if [[ $bibliography_file == "" ]]; then
    bibliography_file="references.bib"
fi

echo "bibliography file: $bibliography_file"

# if no bibliography style is given, use the default
if [[ $bibliography_style == "" ]]; then
    bibliography_style="apalike"
fi

echo "bibliography style: $bibliography_style"

# find input files - all arguments left are input files
for i in "${arguments[@]}"; do
    if [[ $i != -* ]]; then
        inputfiles+=($i)
    fi
done

# if no input files are given, all markdown files in directory from which script is run are used
if [[ ${#inputfiles[@]} == 0 ]]; then
    inputfiles=(*.md)
fi

echo "input files: ${inputfiles[@]}"

# output file is first element of input files array
outputfile=${inputfiles[0]}
# remove extension from output file
outputfile=${outputfile%.*}

echo "output file: $outputfile"

# # header file path
# headerfile='/Users/ananyageorge/.scripts/command-line-tools/pandoc-html-pdf-generator-resources/general-header.txt'

# flags used for all output formats
flags='--toc --filter pandoc-xnos'
# flags used for bibliography
bibliography_flags="--bibliography=$bibliography_file --csl=$bibliography_style"
# flags used for html
html_flags="--mathjax -s -t html"
# add --number-sections to html if you want numbered sections
# flags used for pdf
pdf_flags="-t pdf --listings"
# flags used for tex
tex_flags="-t latex --listings"
# flags used for docx
docx_flags="-t docx"

# ensure bibliography comes after pandoc-xnos filter
if [[ $output_formats == *"b"* ]]; then
    flags="${flags/$bibliography_flags/}"
    echo $flags
    flags="$flags $bibliography_flags"
    echo $flags
fi

# generate output files
# if output format matches the letter, generate the output file
if [[ $output_format == *"h"* ]]; then
    echo "generating html"
    `pandoc -f markdown $flags $html_flags "${inputfiles[@]}" -o "$outputfile.html" --filter pandoc-xnos` && echo "converted to html"
fi
if [[ $output_format == *"p"* ]]; then
    `pandoc -f markdown $pdf_flags $flags "${inputfiles[@]}" -o "$outputfile.pdf" --filter pandoc-xnos` && echo "converted to pdf"
fi
if [[ $output_format == *"t"* ]]; then
    `pandoc -f markdown  $tex_flags $flags "${inputfiles[@]}" -o "$outputfile.tex" --filter pandoc-xnos` && echo "converted to tex"
fi
if [[ $output_format == *"d"* ]]; then
    `pandoc -f markdown $flags $docx_flags "${inputfiles[@]}" -o "$outputfile.docx" --filter pandoc-xnos` && echo "converted to docx"
fi

echo "done"
