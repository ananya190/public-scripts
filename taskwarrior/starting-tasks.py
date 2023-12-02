import subprocess
import os
import datetime
from prompt_toolkit import prompt

"""
start tasks with a depth ritual. if a corresponding taskwarrior task exists, 
start it. works in tandem with the stopping-tasks.py script
"""

# first, see if there is a taskwarrior task; use fzf
x = subprocess.check_output(
    ["task", "_ids", "status:pending", "start.none:"]).decode().split("\n")
x = [i for i in x if i]
x = [j + ": " +
     subprocess.check_output(["task", "_get", f"{j}.project"]).decode().rstrip(
     ) + ": " +
     subprocess.check_output(["task", "_get", f"{j}.description"]).decode(
     ).rstrip() for j in x]
list_of_tasks = "\n".join(x)

task_exists = False

try:
    task_selected = subprocess.check_output(
        f'echo "{list_of_tasks}" | fzf --no-preview --height=30%', shell=True).decode()
    task_exists = True
except subprocess.CalledProcessError:
    print("Nothing selected, moving on")
    task_selected = ""

if task_exists:
    task_to_start = task_selected.split(": ")[0]
    subprocess.call(["task", "start", task_to_start])

# moving on with the rest of the depth ritual: state intention, time, location,
# environment

intention = prompt("state your intention: ")
time = prompt("state the time for which you will work: ")
location = prompt("state the location wherein you will work: ")
environment = prompt("describe the environment wherein you will work: ")

# get current date and time
dt = datetime.datetime.now()
filename_dt = dt.strftime("%Y-%m-%d-%H%M%S")

# write to a file
path = f"{os.getenv('HOME')}/Documents/depths/{filename_dt}.txt"
path_to_log_file = f"{os.getenv('HOME')}/Documents/depths/depths-info.txt"

header_dt = dt.strftime("%A, %B %d, %Y at %H:%M")

string_to_write = f"""{header_dt}

intention: {intention}

time: {time}

location: {location}

environment: {environment}

notes:  
"""

with open(path, "a+") as depth_file:
    depth_file.write(string_to_write)


with open(path_to_log_file, "w+") as log_file:
    log_file.write(filename_dt)
    if task_exists:
        log_file.write(f":{task_to_start}")
    log_file.write("\n")

while True:
    edit = prompt("open file in editor? y/n ")
    if edit == "y":
        subprocess.run(['nvim', '+normal G$', path])
        exit(0)
    elif edit == "n":
        exit(0)
    else:
        print("invalid input.")
