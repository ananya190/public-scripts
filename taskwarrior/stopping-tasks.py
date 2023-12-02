import subprocess
import os

tasks_started = subprocess.check_output(
    ['task', '_ids', 'start.any:']).decode().split("\n")
tasks_started = [x for x in tasks_started if x]
tasks_started_info = [x + ": " +
                      subprocess.check_output(
                          ['task', '_get', f'{x}.project']).decode().rstrip(
                      ) + ": " +
                      subprocess.check_output(
                          ['task', '_get', f'{x}.description']).decode().rstrip(
                      ) for x in tasks_started]
tasks_started_string = "\n".join(tasks_started_info)

try:
    task_selected = subprocess.check_output(
        f'echo "{tasks_started_string}" | fzf --no-preview --height=40%', shell=True).decode()
except Exception as e:
    print(e.with_traceback)
    task_selected = ""

if task_selected:
    subprocess.call(['task', 'stop', task_selected.split(": ")[0]])

# get the depth_log, chdir and nvim the depth file

path_to_log_file = f"{os.getenv('HOME')}/Documents/depths/depths-info.txt"
path_to_depth_file = ""

with open(path_to_log_file, "r+") as log_file:
    path_to_depth_file = log_file.readlines()[-1].rstrip().split(":")[0]
    path_to_depth_file += ".txt"

os.chdir(f"{os.getenv('HOME')}/Documents/depths/")

concluding_string = """
concluding notes: 
"""
if path_to_depth_file:
    with open(path_to_depth_file, "a+") as depth_file:
        depth_file.write(concluding_string)
    subprocess.call(['nvim', '+normal G$', path_to_depth_file])
else:
    subprocess.call(['nvim', '.'])
