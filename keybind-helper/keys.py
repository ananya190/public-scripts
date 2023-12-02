#!/Users/ananyageorge/opt/anaconda3/bin/python

import os
import json
import subprocess
from termcolor import cprint, colored
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

# get list of files from keys directory
path = f"{os.environ.get('HOME')}/.local/share/keys/data/"
# path = f"{os.environ.get('HOME')}/.scripts/keybind-helper/keys/data/"

# if we ever add directories to the keys directory we will have to change this
# find json files
list_of_files = [f for f in os.listdir(path) if f.endswith(".json")]

fuzzy_file_completer = FuzzyWordCompleter(
    [f.removesuffix(".json") for f in list_of_files])

prompt_for_program = prompt("enter the program: ",
                            completer=fuzzy_file_completer)

program_chosen = prompt_for_program + ".json"

if program_chosen not in list_of_files:
    print("sorry, the program: {} is not in our database".format(prompt_for_program))
    exit(0)

# read the json data into the program
with open(os.path.join(path, program_chosen)) as f:
    contents = json.load(f)["commands"]

# fuzzy search descriptions and names of commands or display them all


def fuzzy_search():
    fzf_string = '\n'.join(
        [f"{cmd['command']} - {cmd['description']} - {cmd['shortcut']}" for cmd in contents])
    fzf_command = f"echo \"{fzf_string}\" | fzf -m --no-preview --height=40%"
    # remove empty strings here
    commands_selected = subprocess.check_output(
        fzf_command, shell=True).decode().split("\n")
    commands_selected = [x for x in commands_selected if x]
    list_of_commands = [x.split(" - ") for x in commands_selected]
    return list_of_commands


def all_cmds():
    list_of_commands = []
    for i in contents:
        new_arr = [i["command"], i["description"], i["shortcut"]]
        list_of_commands.append(new_arr)
    return list_of_commands


while True:
    choice = input("enter 0 for fuzzy search, 1 to print them all: ")
    if choice == "0":
        list_of_commands = fuzzy_search()
        break
    elif choice == "1":
        list_of_commands = all_cmds()
        break
    else:
        print("please enter 0 or 1 only")


# now you've got each command in a list in the following format: [command, description, shortcut]
cowsay_string = f"{prompt_for_program}\n\n//\n\n"
for i in list_of_commands:
    command, desc, shortcut = i
    cowsay_string += f"command: {command}\n\n"
    cowsay_string += f"description: {desc}\n\n" if desc else ""
    cowsay_string += f"shortcut: {shortcut}\n\n//\n\n"

os.system(f"echo \"{cowsay_string}\" | cowsay")
