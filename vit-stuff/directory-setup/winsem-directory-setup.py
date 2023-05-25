# python script to setup winter semester directory

# import modules
import os
import json
import re


def result_checking(result, command):
    res_str = "success: " if result == "" else "error: "
    print(res_str, command)
    if result != "":
        exit(1)


# tree structure
# {winter2022:{courses:[course1,course2,etc.]}, {information},
# {study-materials}, {ffcs}}
layer1_dirs = ["courses", "information",
               "study-materials", "ffcs", "latex-templates"]

layer1_files = ["index.md", "capture.md"]

# make the first layer of directories
print("Making layer 1 directories...")

layer1_cmd = 'mkdir -p winter2022/'

for dirname in layer1_dirs:
    dircommand = f'{layer1_cmd}{dirname}'
    result = os.popen(dircommand).read()
    result_checking(result=result, command=dircommand)

for file_name in layer1_files:
    filecommand = f'echo \"# {file_name}\" >> '
    filecommand = f'{filecommand}winter2022/{file_name}'
    result = os.popen(filecommand).read()
    result_checking(result=result, command=filecommand)

# course template list
course_template_list = {"courses": ["assignments.csv",
                                    "assignments.md",
                                    "courses.md",
                                    "info.json"],
                        "latex-templates": ["digital-assignment.tex",
                                            "lab-assignment.tex",
                                            "project-report.tex"]}

# use template list to make files
print("adding latex and course files...")

layer2_cmd = 'touch winter2022/'

echo_capture = int(input("Echo the file name into the md files? (0/1)"))

for parent_directory in course_template_list:
    for file_name in course_template_list[parent_directory]:
        filecommand = f'{layer2_cmd}{parent_directory}/{file_name}'
        result = os.popen(filecommand).read()
        result_checking(result=result, command=filecommand)
        if echo_capture and re.search(".*[.]md$", file_name) is not None:
            echo_command = f'echo \"# {file_name}\" >> winter2022/'
            echo_command = f'{echo_command}{parent_directory}/{file_name}'
            result = os.popen(echo_command).read()
            result_checking(result=result, command=echo_command)

# write the required header into assignments.csv and copy info.json to the
# right place
with open("winter2022/courses/assignments.csv", "w+") as f1:
    f1.write("x,due,status,complete_by,course,name,information,links,comments")

cp_command = 'cp info.json winter2022/courses/info.json'
result = os.popen(cp_command).read()
result_checking(result=result, command=cp_command)


# make the second layer of directories
print("Making layer 2 directories...")

# use info.json to create each directory
with open("info.json", "r") as f:
    info = json.load(f)

# display json using print(info)

# creating subdirectories for each course based on type
course_subdirectory_dict = {"project": ["report"],
                            "lab": ["notes", "assignments"],
                            "theory": ["notes", "assignments"]}

win_course_command_dir = 'mkdir -p winter2022/courses/'

win_course_cmd_file = 'winter2022/courses/'

for course in info["courses"]:
    mkdir_command = f'{win_course_command_dir}{course["dir"]}'
    result = os.popen(mkdir_command).read()
    result_checking(result=result, command=mkdir_command)
    course_type = str(course["type"])
    course_type = course_type.capitalize() if course_type == "project" else ""
    if echo_capture:
        wiki_index = f'echo \"# {course["name"]} {course_type}\" >>'
    else:
        wiki_index = 'touch'
    wiki_index = f'{wiki_index} {win_course_cmd_file}{course["dir"]}/'
    wiki_index = f'{wiki_index}{course["dir"]}.md'
    result = os.popen(wiki_index).read()
    result_checking(result=result, command=wiki_index)
    for sub_dir in course_subdirectory_dict[course["type"]]:
        mksubdir = f'{win_course_command_dir}{course["dir"]}/{sub_dir}/images'
        result = os.popen(mksubdir).read()
        result_checking(result=result, command=mksubdir)
