import os
import json

print("reading json")
with open("info.json", "r+") as f:
    info = json.load(f)
print("json loaded")

print("iterating through course list")
for course in info["courses"]:
    if course["type"] == "project":
        print("project course encountered")
        cmd_cp = 'cp vitlogo.png winter2022/courses/'
        cmd_cp += f'{course["dir"]}/report/images/'
        print("beginning copy")
        result = os.popen(cmd_cp).read()
        print(result)
        if result == "":
            print("successfully copied image to image directory for project")
        else:
            print(f'error copying to directory {course["dir"]}')

print("all done")
