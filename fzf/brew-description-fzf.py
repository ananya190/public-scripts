#!/Users/ananyageorge/opt/anaconda3/bin/python

import os
import sys
import subprocess
from prompt_toolkit import prompt
import re
from termcolor import cprint

# switching name_search to true until brew search --desc is fixed
name_search = True

if len(sys.argv) > 1 and sys.argv[1] == 'n':
    name_search = True

header_list = ["==> Formulae", "==> Casks"]
# take description
if name_search:
    flag_list = ["formulae", "casks"]
    name_of_brew = prompt("Enter the name of the brew: ")
    list_of_brews = []
    for i in range(2):
        list_of_brews.append(header_list[i])
        try:
            list_from_brew_search = subprocess.check_output(
                f"brew search --{flag_list[i]} \"{name_of_brew}\"",
                shell=True, stderr=subprocess.DEVNULL).decode().split("\n")
        except Exception as e:
            print(e)
            list_from_brew_search = ['']
        list_of_brews.extend(list_from_brew_search)
else:
    desc = prompt("Enter the description for the brew: ")
    list_of_brews = os.popen(
        f"brew search --desc --eval-all {desc}").read().split('\n')


def cut_func(desc_string):
    match = re.findall("(^.*):.*$", desc_string)
    if len(match) > 0:
        return match[0]
    else:
        return desc_string


list_of_brews = [cut_func(brew) for brew in list_of_brews]

list_of_brews_str = "\n".join(list_of_brews)

# brew = os.system(" echo \"%s\" | fzf --preview 'brew info {}'" % list_of_brews_str)
try:
    brews_bytestring = subprocess.check_output(
        "echo \"%s\" | fzf -m --height=40%% --preview 'brew info {}'" %
        list_of_brews_str, shell=True)
except Exception as e:
    print("Nothing selected, type e to see error, any other key to exit: ")
    if input() == "e":
        cprint(str(e), color="red")
    exit(0)

# decoding the bytestring
brew = brews_bytestring.decode()

# split at newlines, remove empty line and "==> Casks" and "==> Formulae"
selected_brew_list = brew.split("\n")
selected_brew_list = [
    i for i in selected_brew_list if i and i not in header_list]

print("brews selected:\n%s" % "\n".join(selected_brew_list))

# get index of where formulae end and casks begin in the original list
index_of_cask = list_of_brews.index("==> Casks")
print(f"index of casks: {index_of_cask}")

install_command = "brew install"

brews_installed = []

# for each brew, print info, then user inputs i to install, n or enter to move on
for grape in selected_brew_list:
    os.system("brew info %s" % grape)
    # present menu
    while True:
        choice = input("Enter i to install, n or <Enter> to continue: ")
        if choice == "i":
            index_of_brew = list_of_brews.index(grape)
            print(
                f"index of this brew: {index_of_brew}; index of cask: {index_of_cask}")
            brews_installed.append(grape)
            if index_of_brew < index_of_cask:
                print(os.popen(" %(install_command)s %(grape)s" %
                               {"install_command": install_command,
                                "grape": grape}).read())
            else:
                print(os.popen(" %(install_command)s --cask %(grape)s" %
                      {"install_command": install_command, "grape": grape}).read())
            break
        elif choice == "n" or choice == "":
            break
        else:
            print("you must input either n or i or hit <Enter>")

# display info about brews installed
print("brews installed:")
for i in range(len(brews_installed)):
    print(f"{i+1}: {brews_installed[i]}")
print(f"{len(brews_installed)} brews installed")
