# read the contents of info.json to get the slot, course name and professor
# sort the lines by slot

import json

with open("../info.json", "r") as f:
    info = json.load(f)

print(info)

course_dict = {"Theory": [], "Lab": [], "Project": []}
for course in info["courses"]:
    slot = course["slot"]
    course_code = course["course_code"]
    name = course["name"]
    prof = course["prof"]
    course_type = str(course["type"]).capitalize()
    venue = course["venue"] if course["venue"] else "-"
    bullet_string = f'- {slot}: {course_code} {name} [{prof}, {venue}]\n'
    course_dict[course_type].append(bullet_string)

with open("README.md", "w+") as fw:
    fw.write("# Winter Semester 2022-23\n\n")
    for course_type in course_dict:
        header_str = f'## {course_type} Courses\n\n'
        fw.write(header_str)
        fw.writelines(course_dict[course_type])
        fw.write("\n")
