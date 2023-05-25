#!/bin/sh
# pandoc note generation

# set array to hold all files passed in argument
arguments=("$@")

# if any argument begins with a "-", treat it as an option and add to a variable
# if an option contains p, add pdf to output formats
# if an option contains b, add bibliography to output formats
# if an option contains h, add html to output formats
# if an option contains t, add tex to output formats
# if an option contains x, add docx to output formats
# if no options are given, add html, pdf and bibliography to the output formats.
# initialize output formats variable
output_formats=""
# find options
for i in "${arguments[@]}"; do
    if [[ $i == -* ]]; then
        # remove the dash and parse the option, adding each letter individually if it's not already in the array
        for (( j=1; j<${#i}; j++ )); do
            echo ${i:$j:1}
            if [[ $output_formats != *${i:$j:1}* ]]; then
                output_formats+="${i:$j:1}"
            fi
        done
    fi
done

# if no output formats are given, add html, pdf and bibliography to the output formats.
if [[ $output_formats == "" ]]; then
    output_formats="hpb"
fi

# if only bibliography is given, add html and pdf to the output formats.
if [[ $output_formats == "b" ]]; then
    output_formats="hpb"
fi

echo "output formats: $output_formats"


# find input files
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

# flags used for all output formats
flags="--toc --listings  --filter pandoc-xnos"
# flags used for bibliography
bibliography_flags="--bibliography=references.bib --csl=apa.csl"
# flags used for html
html_flags="--mathjax -s -t html"
# flags used for pdf
pdf_flags="-t pdf"
# flags used for tex
tex_flags="-t latex"
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
if [[ $output_formats == *"h"* ]]; then
    `pandoc -f markdown $html_flags "$inputfiles" -o "$outputfile.html" $flags` && echo "converted to html"
fi
if [[ $output_formats == *"p"* ]]; then
    `pandoc -f markdown $pdf_flags "$inputfiles" -o "$outputfile.pdf" $flags` && echo "converted to pdf"
fi
if [[ $output_formats == *"t"* ]]; then
    `pandoc -f markdown $tex_flags "$inputfiles" -o "$outputfile.tex" $flags` && echo "converted to tex"
fi
if [[ $output_formats == *"x"* ]]; then
    `pandoc -f markdown $docx_flags "$inputfiles" -o "$outputfile.docx" $flags` && echo "converted to docx"
fi

echo "done"