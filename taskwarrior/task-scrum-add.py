import os
import datetime
from re import S
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

"""
menu driven program to add taskwarrior scrum tasks

flow:
    ask for project name
    ask whether tasks will be input manually or from a text file
    if text file, provide link to text file
    text file format:
    <desc> <tags> <other key:value pairs>
    <desc> <tags> <other key:value pairs>
    ...
    <desc> <tags> <other key:value pairs>
    <desc> <tags> <other key:value pairs>
    iterate through the file and append to a list
    if manual, prompt for description
    then prompt for tags
    prompt for other key value pairs
    save to a single string and append to a list
    for each line in the list, add the task to taskwarrior
"""

# get the result of task _projects
project_list = os.popen("task _projects").read().split('\n')
project_list = [x for x in project_list if x]

# select project using fuzzy completion
project_completer = FuzzyWordCompleter(project_list)
project_name = prompt("Enter the project name: ", completer=project_completer)
print("Project: %s" % project_name)

# initialize the empty array for tasks
list_of_tasks = []


# define function for reading from text file


def read_tasks_from_textfile():

    # read file path from user
    files = os.popen("ls").read().split('\n')
    print(files)
    filename = prompt("choose your file: ",
                      completer=FuzzyWordCompleter(files))

    with open(filename, "r") as taskfile:
        tasks_from_file = [x.rstrip('\n') for x in taskfile.readlines() if x]

    list_of_tasks.extend(tasks_from_file)
    return

# define function for reading from input


def read_tasks_from_input():

    # initialization of required variables
    # flag to keep loop running
    flag = True
    # list of tags to fuzzy prompt with
    tags = ['sprint', 'backlog', 'inprogress', 'onhold', 'scrump', 'regular']

    # initialize do-while loop
    while (True):

        # prompt for task description
        while (True):
            task_description = prompt("enter the task description: ").rstrip()
            if task_description:
                break
            else:
                print("Description must be provided")

        # prompt for points
        task_points = prompt("enter the number of points: ")
        task_points = int(task_points) if task_points.isnumeric() else ''

        # prompt for recurrence
        task_recurs = False
        while (True):
            recurs = prompt(
                "is this a recurring task? (y for yes, n or enter for no): ")
            if recurs == "y":
                task_recurs = True
                break
            elif recurs == "n" or recurs == "":
                break
            else:
                print("please enter y, n, or enter only.")

        # prompt for tags
        if task_recurs:
            task_tag = "regular"
            task_recurrence = prompt("how often do you want this to recur?: ")
            task_due = prompt("when is this task due? ")
            task_description = f'{task_description} recur:{task_recurrence} due:{task_due}'
        else:
            while (True):
                task_tag = prompt("enter the status tag: ",
                                  completer=FuzzyWordCompleter(tags))
                if task_tag in tags:
                    break
                else:
                    print("Tags must be one of the scrum tags")

        # construct new task from description and tags
        new_task = f'{task_description} +{task_tag}'
        if task_points:
            new_task = f'{new_task} points:{task_points}'

        # append to array
        list_of_tasks.append(new_task)

        while (True):
            cont = input(
                "Enter 0 to append tasks and end program, 1 (or) Enter to keep going: ")
            if cont == '0':
                flag = False
                break
            elif cont == '' or cont == '1':
                break
            else:
                print("This prompt can only accept an input of 0, 1 or Enter")
        if not flag:
            break


# ask if tasks are in a text file or will be entered manually
while (True):
    print("Choice of input")
    print("0: Manual")
    print("1: Text File")
    choice_of_input = int(input("Enter 0/1: "))
    if choice_of_input == 0:
        read_tasks_from_input()
        break
    elif choice_of_input == 1:
        read_tasks_from_textfile()
        break
    else:
        print("please enter 0 or 1 only")


# process the task list
# 1. append scrum:true to each one
# 2. append project:<project-name> to each one

blind_confirm = True if input(
    "Enter y if you want to add all tasks without confirmation: ") == 'y' else False


for task in list_of_tasks:
    add = True
    task_to_add = f"{task} scrum:true project:{project_name}"
    task_command = f"task add {task_to_add}"
    if not blind_confirm:
        print(task_command)
        confirm = input('Confirm this task with "y" or <Enter>: ')
        if confirm != '' and confirm != 'y':
            add = False
    if add:
        print(os.popen(task_command).read())

os.system(f"task scrum project:{project_name}")
