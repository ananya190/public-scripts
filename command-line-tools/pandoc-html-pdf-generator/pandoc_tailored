#!/Users/ananyageorge/opt/anaconda3/bin/python

import os
import re
import sys
from pandoc_tailored_docs import display_help

"""pandoc_tailored
options:
    1. sd = separate directories for each output format: t[rue] f[alse]
    default: t
    2. sf = separate output for each file: t[rue] f[alse] default: f
    3. f = output format h p d t default: hp
    4. of = output file name (only when sf not chosen) string default: first
    input file name
    5. od = output directory name (prepended to output_format) string default:
    none
    6. bib = create bibliography t[rue] f[alse] default: t
    7. bibf = bibliography_file
    8. bibs = bibliography_style
    9. ns = numbered sections in html
"""


def separate_file_creation(format):
    """create separate files for each input file for each output format

    :format: h, p, d, t
    :returns: None

    """
    common_cmd = f"/Users/ananyageorge/bin/pandoc -f markdown {formats[format]}"

    print(files)
    for i in range(len(files)):
        print(i)
        sep_command = f"{common_cmd} \"{files[i]}.md\""
        sep_command += f" -o \"{output_dir[format]}{new_files[i]}.{op_dict[format]}\""
        for q in common_flags:
            sep_command += f" {q}"
        sep_command += bib_str
        result = os.popen(sep_command).read()
        print(f"result of command: {sep_command}: {result}")
    return


def merge_files(format):
    """merge all files into one output file for each output format

    :format: h, p, d, t
    :returns: None

    """
    print(f"files in merge_files: {files}")
    common_cmd = f"/Users/ananyageorge/bin/pandoc -f markdown {formats[format]} "
    file_str = " ".join([f"\"{x}.md\"" for x in files])
    merge_cmd = f"{common_cmd}{file_str} "
    merge_cmd += f"-o \"{output_dir[format]}{flags['of']}.{op_dict[format]}\""
    for q in common_flags:
        merge_cmd += f" {q}"
    merge_cmd += bib_str
    result = os.popen(merge_cmd).read()
    print(f"result of command: {merge_cmd}: {result}")
    return


arguments = sys.argv

true_pattern = re.compile("t(rue)?")
false_pattern = re.compile("f(alse)?")

if len(arguments) > 1 and re.match(arguments[1], "h(elp)?"):
    if len(arguments) > 2:
        display_help(options=arguments[2])
    else:
        display_help()
    exit(0)


files = []

op_dict = {"h": "html", "d": "docx", "p": "pdf", "t": "tex"}

output_formats = {"h": "--mathjax -s -t html",
                  "p": "--listings -t pdf", "t": "--listings -s -t latex",
                  "d": "-t docx"}

output_dir = {"h": "../html/", "p": "../pdf/", "d": "../docx/", "t": "../tex/"}

flags = {"sd": "", "sf": "", "f": "", "of": "",
         "od": "", "bib": "", "bibf": "", "bibs": "", "ns": ""}

i = 1
while i < len(arguments):
    if re.fullmatch("-.+", arguments[i]):
        flag = re.sub("-(.+)", r"\1", arguments[i])
        print(flag)
        flags[flag] = arguments[i+1].lower()
        print(flags[flag])
        i += 2
    else:
        print(arguments[i])
        if arguments[i].endswith(".md"):
            files.append(arguments[i])
        print(files)
        i += 1


common_flags = ["--toc", "--filter pandoc-xnos"]

if len(files) == 0:
    files = [x for x in os.listdir() if x.endswith(".md")]

if len(files) == 0:
    print("There are no markdown files")
    exit(0)

files = sorted([file[:-3] for file in files])

print(files)

default_flags = {"sd": "true", "sf": "false", "f": "hp",
                 "of": os.path.basename(files[0]),
                 "od": "", "bib": "true", "bibf": "references.bib",
                 "bibs": "apalike", "ns": "false"}

# start checking and adding defaults for values
for i in flags:
    if flags[i] == "":
        flags[i] = default_flags[i]
print(flags)

bibliography_flags = f" --bibliography={flags['bibf']} --csl={flags['bibs']}"
# bibliography_flags += "--citeproc"
bib_str = bibliography_flags if true_pattern.fullmatch(flags["bib"]) else ""

formats = {k: output_formats[k] for k in flags["f"]}

print(formats)

# number sections in html

if true_pattern.fullmatch(flags["ns"]) and "h" in formats:
    formats["h"] += " --number-sections"

if flags["od"]:
    flags["od"] += "_"

parent_dir = os.path.abspath(f"{files[0]}/../..")
print(parent_dir)

new_files = [os.path.basename(x) for x in files]
print(new_files)

print(flags["of"])

for k in flags["f"]:
    if true_pattern.fullmatch(flags["sd"]):
        dir_name = f"{flags['od']}{op_dict[k]}"
        print("parent directory")
        print(parent_dir)
        print("dir name")
        print(dir_name)
        output_dir[k] = f"{parent_dir}/{dir_name}/"
        print(output_dir)
        os.popen(f"mkdir -p \"{output_dir[k]}\"")
    else:
        output_dir[k] = ""
    if true_pattern.fullmatch(flags["sf"]):
        print("separate files")
        separate_file_creation(k)
    else:
        print("one file")
        merge_files(k)
