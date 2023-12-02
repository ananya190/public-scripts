#!/Users/ananyageorge/opt/anaconda3/bin/python3.9

import os
import sys
import json

filename = sys.argv[1] if len(sys.argv) > 1 else input(
    "Please enter the filename without the extension, eg. a1, ipwt_a2, etc.: ")
template_path = "~/vit/winter2022/latex-templates/da-template.tex "


info = {}

with open("/Users/ananyageorge/vit/winter2022/courses/info.json", "r") as infojson:
    info = json.load(infojson)["courses"]

tex_newcmd = "\\newcommand"

assignment_info = {
    "daCourseCode": "",
    "daSlot": "",
    "daAssignmentName": "",
    "daCourseName": "",
    "daProfessor": "",
    "dueDate": ""
}

# copy first 4 lines into the new file [this will overwrite any
# existing tex file with the same name]
head_cmd = f"head -n 6 {template_path} > {filename}.tex"

result = os.popen(head_cmd).read()
print(result)

# input for course, title and due date
class_name = input("Please enter the name of class, e.g esp or dv_l: ")

assignment_class_arr = [d for d in info if d['id'] == class_name]

assignment_class = assignment_class_arr[0] if len(assignment_class_arr) > 0 else {
    'course_code': "",
    'name': "",
    'slot': "",
    'prof': ""
}

assignment_info["daCourseCode"] = assignment_class['course_code']
assignment_info["daCourseName"] = assignment_class['name']
assignment_info["daSlot"] = assignment_class['slot']
assignment_info["daProfessor"] = assignment_class['prof']
assignment_info["daAssignmentName"] = " ".join([i.capitalize() for i in input(
    "Please enter the name of the assignment: ").split(" ")])
assignment_info["dueDate"] = " ".join(
    [i.capitalize() for i in input("Please enter the due date: ").split(" ")])


str_to_write = ""

for key in assignment_info:
    str_to_write += tex_newcmd
    str_to_write += "{\\" + key + "}"
    str_to_write += "{" + assignment_info[key] + "}\n"

with open(f"{ filename }.tex", "a+") as dafile:
    dafile.write(str_to_write)

tail_cmd = f"tail -n 28 {template_path} >> {filename}.tex"
result = os.popen(tail_cmd).read()
print(result)

print(f"template written to {filename}.tex")
