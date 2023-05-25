import os
import re

for file in os.listdir():
    if os.path.isdir(file):
        new_file = re.sub(" ", "-", file).lower()
        print(file)
        print(new_file)
        cmd = f"mv \"{file}\" \"{new_file}\""
        print(cmd)
        print(os.popen(cmd).read())
