import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
import argparse

"""
program to display scrum report for all projects or a specific one

all: pass -a flag or hit enter when prompted
specific: fuzzy search through list of projects
"""

task_scrum_command = "task scrum"

# create argument parser instance to capture -a flag
parser = argparse.ArgumentParser(
    prog="Taskwarrior Scrum Report",
    description="Displays the scrum report for all projects or a specified one"
)
parser.add_argument('-a', '--all_projects', action='store_true',
                    help="display all projects")

args = parser.parse_args()

if args.all_projects:
    print(os.popen(task_scrum_command).read())
    exit(0)


# get list of projects
project_list = os.popen("task _projects scrum:true").read().split('\n')
project_list = [x for x in project_list if x]

# select project using fuzzy completion
project_completer = FuzzyWordCompleter(project_list)
project_name = prompt("Enter the project name: ", completer=project_completer)
print("Project: %s" % project_name)

os.system(f"{task_scrum_command} project:{project_name}")
