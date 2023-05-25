#!/Users/ananyageorge/opt/anaconda3/bin/python

from tabulate import tabulate

import os
import random
import string
import json
import re

json_file = "/Users/ananyageorge/vit/winter2022/courses/assignments.json"

with open(json_file, "r+") as assjson:
    a = json.load(assjson)

uuidmatch = re.compile(".+")
idmatch = re.compile("[0-9a-zA-Z]{3}")
datematch = re.compile("[0-9]{4}(-[0-9]{2}){2}")
statusmatch = re.compile("[x_?]")
desccoursematch = re.compile("[a-zA-Z]+.*")

assignment_list = []
completed_list = []
if a["assignments"]:
    assignment_list = a["assignments"]
if a["completed"]:
    completed_list = a["completed"]

# TODO: add completion and edit task functionality #


def check_fields(regex_pattern, input_s):
    if regex_pattern.fullmatch(input_s):
        return True


def generate_assignment_id():
    a_id = "".join(random.choices(string.ascii_lowercase+string.digits, k=3))
    return a_id


def create_assignment_id():
    print("generating assignment id")
    while True:
        a_id = generate_assignment_id()
        print(a_id)
        if not any(d["id"] == a_id for d in a["assignments"]):
            return a_id


# add assignments
hash_ids = {
    1: ["uuid", uuidmatch],
    2: ["id", idmatch],
    3: ["x", statusmatch],
    4: ["due", datematch],
    5: ["complete_by", datematch],
    6: ["course", desccoursematch],
    7: ["name", desccoursematch],
    8: ["information", desccoursematch],
    9: ["links", desccoursematch],
    0: ["comments", desccoursematch]
}

format_row = "{:<4} {:<25} {:<4} {:<2} {:<12} {:<12} {:<12} {:<25} {:<25} {:<25} {:<25}"
header_arr = [hash_ids[x % 10][0][:25] for x in range(1, 11)]


def display_json():
    if len(a["assignments"]) == 0:
        print("no assignments")
        return -1
    print(format_row.format("", *header_arr))
    for value in assignment_list:
        v = [value[hash_ids[x % 10][0]][:25] for x in range(1, 11)]
        print(format_row.format(v[1], *v))
    return 0


if re.fullmatch("-+[dD]", "sys.argv[1]"):
    display_json()


def create_assignment():

    assignment = {}
    for i in range(3, 11):
        j = (i) % 10
        a_inp = input(f"{hash_ids[j][0]}: ").strip()
        # check input fields
        while not check_fields(hash_ids[j][1], a_inp):
            print(f"error in {hash_ids[j][0]}")
            a_inp = input(f"{hash_ids[j][0]}: ").strip()
        assignment[hash_ids[j][0]] = a_inp

    print(assignment)

    assignment_add_cmd = f"+{assignment['course']} project:vit.assignments"
    assignment_add_cmd += f" due:{assignment['due']} {assignment['name']}"
    print(assignment_add_cmd)
    result = os.popen(f"task add {assignment_add_cmd}").read()
    print(result)
    uuid = os.popen("task +LATEST uuids").read().strip()
    if uuid:
        assignment['uuid'] = uuid.strip().rstrip()

    assignment["id"] = create_assignment_id()
    print(assignment)

    assignment_list.append(assignment)
    assignment_list.sort(key=lambda x: x["due"])


def write_to_json():
    assignment_list.sort(key=lambda x: x["due"])
    with open(json_file, "r+") as jfile:
        jfile_data = json.load(jfile)
        jfile_data["assignments"] = assignment_list
        jfile.seek(0)
        json.dump(jfile_data, jfile, indent=4)


while True:
    assignment_list.sort(key=lambda x: x["due"])
    choice = input("a to add assignment, d to display, q to quit: ")
    if choice == 'a':
        create_assignment()
    elif choice == 'd':
        display_json()
    elif choice == 'q':
        write_to_json()
        exit(0)
    else:
        print("wrong choice")
