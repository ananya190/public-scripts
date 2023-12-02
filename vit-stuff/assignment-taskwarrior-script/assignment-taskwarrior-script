#!/Users/ananyageorge/opt/anaconda3/bin/python

# TODO: generalize - use JSON <07-12-22 Ananya> #
# DONE: add sorting csv <10-12-22 Ananya> #
# TODO: remove extraneous print statements <10-12-22 Ananya> #
# TODO: display assignments to mark complete <10-12-22 Ananya> #
# menu driven
# 1. add assignment
# 2. modify assignment - status, x
# 3. see assignments

import sys
import os
import re
from datetime import datetime, timedelta
import string
import random

import_file_errors = []

assignment_dir = "/Users/ananyageorge/vit/winter2022/"

""" csv file for import format
course(id),due,complete_by,name,information,links,comments
"""

""" assignments.csv header
id, uuid, x, due, complete_by, course, name, information, links, comments
note:
uuid from taskwarrior, id is random 3 character (numbers and letters) string
assigned by script
"""

""" assignment dictionary type
{assume type is string unless otherwise mentioned}
assignment_dict = {
id: <generated>,
uuid: <taskwarrior>,
x: <input>,
due: <date input>,
complete_by: <date input>,
course: <input>,
name: <input>,
information: <input>,
links: <array input>,
comments: <array input>
}
"""

"""assignment dictionary hash
1: id,
2: uuid,
3: x,
4: due,
5: complete_by,
6: course,
7: name,
8: information,
9: links,
0: comments
"""

"""x status
? - not begun
_ - in progress
x - done
"""

assignment_dict_hash = {
    1: "id",
    2: "uuid",
    3: "x",
    4: "due",
    5: "complete_by",
    6: "course",
    7: "name",
    8: "information",
    9: "links",
    0: "comments"
}


def display_fields():
    for i in range(1, 11):
        j = i % 10
        print(j, ": ", assignment_dict_hash[j])


# the decision to start from 1 was because 1-0 are in a row on the keyboard
# as opposed to starting with 0 then moving all the way to the left for 1

date_fmt = "%Y-%m-%d"

header_fmt = ["due", "completeby", "courseid", "name", "information", "links",
              "comments"]


# filepath = f"{assignment_dir}courses/assignments.csv"
# with open(filepath,"r+") as f:
#     _ = f.readline()


csv_assignment_ls_dict = []
csv_assignment_modified_ls_dict = []


def load_assignments(csv_assignment_list):
    for assignment in csv_assignment_list:
        assignment_ls = assignment.split(',')
        # the assignment information in an array
        assignment_dict = {assignment_dict_hash[(
            i+1) % 10]: assignment_ls[i] for i in range(10)}
        csv_assignment_ls_dict.append(assignment_dict)
        csv_assignment_modified_ls_dict.append(assignment_dict)


def field_checks(field_i, inp):
    """field_checks
    1. if field affects timewarrior, check it
    2. if field is uuid, return False
    3. if field is date, ensure date is valid
    4. if field is x, ensure it is one of x, ? or _
    5. if field is text, replace any commas with semicolons
    return True if checks pass
    print error and return False if not
    """
    if field_i == 3 and re.match("[?_x]", inp):
        return True
    if (field_i == 4 or field_i == 5) and re.match("[0-9]{4}-[0-9 ]{2}-[0-9]{2}", inp):
        return True
    if field_i > 5 or field_i < 3:
        return True
    return False


def generate_assignment_id():
    a_id = "".join(random.choices(string.ascii_lowercase+string.digits, k=3))
    return a_id


def create_assignment_id():
    print("generating assignment id")
    while True:
        a_id = generate_assignment_id()
        print(a_id)
        if not any(d["id"] == a_id for d in csv_assignment_modified_ls_dict):
            return a_id


def input_date():
    while True:
        date = input("please enter date in yyyy-mm-dd format: ")
        try:
            date = datetime.strptime(date, date_fmt)
            print(date)
            date = date.strftime(date_fmt)
            print(date)
            break
        except ValueError as exception:
            print("error creating datetime object: ", exception)
    return date


def complete_by_date(due_date):
    """Docstring for complete_by_date.
    set complete_by date
    :due_date: due date of assignment under consideration
    :returns: datetime
    """
    print("complete by date")
    while True:
        prompt = "1. standard (-2 days from due date)\n2. custom date\n"
        choice = int(input(prompt))
        if choice == 1:
            return (datetime.strptime(due_date, date_fmt) + timedelta(days=-2)).strftime(date_fmt)
        if choice == 2:
            return input_date()
        else:
            print("please choose either 1 or 2\n")


input_prompts = {
    6: "please enter the course code\n",
    7: "please enter the name of the assignment\n",
    8: "please enter information about the assignment\n",
    9: "please enter relevant links\n",
    0: "please enter relevant comments\n"
}

assignment_dict_hash_creation_functions = {
    1: create_assignment_id,
    2: "",
    3: "?",
    4: input_date,
    5: complete_by_date,
    6: input,
    7: input,
    8: input,
    9: input,
    0: input
}


def can_modify_field(field_i):
    if field_i < 3:
        return False
    return True


def modify_field(field_i):
    """modify_field
    1. take field index
    2. use assignment creation function for field index
    3. run field checks on modification
    4. once it passes, return it
    NOTE: this function does not check for field index < 3
    NOTE: run can_modify_field first
    """
    print("enter the modification")
    print(f"{assignment_dict_hash[field_i]}: ", end="")
    if field_i < 5:
        if field_i == 2 or field_i == 3:
            new_value = assignment_dict_hash_creation_functions[field_i].strip(
            )
        else:
            new_value = assignment_dict_hash_creation_functions[field_i](
            ).strip()
    else:
        new_value = assignment_dict_hash_creation_functions[field_i](
            input_prompts[field_i]).strip()
    while not field_checks(field_i=field_i, inp=new_value):
        print("there's an error with your modification")
        if field_i < 5:
            if field_i == 2 or field_i == 3:
                new_value = assignment_dict_hash_creation_functions[field_i].strip(
                )
            else:
                new_value = assignment_dict_hash_creation_functions[field_i](
                ).strip()
        else:
            new_value = assignment_dict_hash_creation_functions[field_i](
                input_prompts[field_i]).strip()
    new_value = re.sub("[,;]*", " ", new_value)
    return new_value.strip()


def create_assignment_from_list(assignment_arr):
    """create_assignment_from_list
    1. take a single element from the assignment list
    2. generate unique id
    3. convert to assignment dictionary format
    4. return individual dictionary
    """
    assignment_d = {}
    for i in range(1, 4):
        if i == 2 or i == 3:
            curr_attribute = assignment_dict_hash_creation_functions[i]
        else:
            curr_attribute = assignment_dict_hash_creation_functions[i]()
        assignment_d[assignment_dict_hash[i]] = str(curr_attribute.strip())
    for i in range(3, 5):
        try:
            date_inp = datetime.strptime(
                assignment_arr[i], date_fmt).strftime(date_fmt)
        except ValueError:
            print("error converting to date, please input manually")
            print(f"input = {assignment_arr[i]}")
            date_inp = input_date()
        assignment_d[assignment_dict_hash[i + 1]] = date_inp
    for i in range(5, 10):
        field_i = (i + 1) % 10
        field = assignment_dict_hash[field_i]
        value = assignment_arr[i]
        if (not field_checks(field_i=field_i, inp=value)) and can_modify_field(field_i):
            print("error with field, calling modification function...")
            print(f"field: {field}")
            print(f"value: {value}")
            value = modify_field(field_i)
        assignment_d[field] = str(value.strip())
    return assignment_d


def modify_assignment_dict(assignment_dictionary, tw=False):
    """modify_assignment_dict
    take fields
    call modify_field for each field
    return new dictionary
    """
    assignment_modified = assignment_dictionary.copy()
    display_assignment_dict_form_field_wise(assignment_dictionary)
    display_fields()
    while True:
        modification_fields = input(
            "please enter fields to modify separated by spaces")
        try:
            modification_fields = [int(i)
                                   for i in modification_fields.split(" ")]
            break
        except ValueError:
            print("use integers only")
    for field_i in modification_fields:
        if can_modify_field(field_i):
            field = assignment_dict_hash[field_i]
            modification = modify_field(field_i)
            if tw:
                modify_assignment_tw(
                    uuid=assignment_dictionary["uuid"], field_i=field_i, modification=modification)
            assignment_modified[field] = str(modification.strip())
    return assignment_modified


def import_from_file(filename):

    print("in import from file function...")

    global csv_assignment_modified_ls_dict

    with open(filename, "r") as f:

        file_assignment_list = []
        header = f.readline().strip()
        if not re.match("^[dD][uU][eE].*", header):
            file_assignment_list.append(header)
        file_assignment_list.extend([i.strip() for i in f.readlines()])
        print("assignments:", file_assignment_list)
        for i in file_assignment_list:
            assignment_as_list = i.split(',')
            assignment_d = create_assignment_from_list(assignment_as_list)
            csv_assignment_modified_ls_dict.append(assignment_d)


def add_assignment_to_list():
    """add_assignment_to_list
    1. input fields and check
    2. display fields
    3. modify fields
    4. create dictionary
    5. add dictionary to list
    """
    assignment_d = {}
    for j in range(1, 11):
        if j < 5:
            if j == 2 or j == 3:
                curr_attribute = assignment_dict_hash_creation_functions[j]
            else:
                curr_attribute = assignment_dict_hash_creation_functions[j]()
        elif j == 5:
            due_d = assignment_d[assignment_dict_hash[j - 1]]
            curr_attribute = assignment_dict_hash_creation_functions[j % 10](
                due_d)
        else:
            curr_attribute = assignment_dict_hash_creation_functions[j % 10](
                input_prompts[j % 10])
        curr_attribute = re.sub("[,;]*", " ", curr_attribute)
        if not field_checks(j % 10, curr_attribute) and can_modify_field(j % 10):
            print("error with current field")
            print(f"field: {assignment_dict_hash[j % 10]}")
            print(f"value: {curr_attribute}")
            curr_attribute = modify_field(j % 10)
        curr_attribute = re.sub("[,;]*", " ", curr_attribute)
        assignment_d[assignment_dict_hash[j % 10]] = curr_attribute.strip()
    global csv_assignment_modified_ls_dict
    csv_assignment_modified_ls_dict.append(assignment_d)
    return


def display_assignment_header():
    for i in range(1, 11):
        j = i % 10
        field = assignment_dict_hash[j]
        print(field, end="\t")
    print()


def display_assignment_dict_form_tabular(assignment):
    """display_assignment_dict_form_tabular
    display a single assignment dictionary, with fields separated by tabs
    """
    for i in range(1, 11):
        j = i % 10
        field = assignment_dict_hash[j]
        value = assignment[field]
        print(value, end="\t")
    print()


def display_assignments_in_csv():
    """display_assignments_in_csv
    display assignments in the csv
    """
    if len(csv_assignment_ls_dict) == 0:
        print("no assignments")
        return
    display_assignment_header()
    for assignment in csv_assignment_ls_dict:
        display_assignment_dict_form_tabular(assignment)
    return


def get_tw_uuid_from_csv(id):
    """get_tw_uuid
    get taskwarrior uuid using id from csv
    """
    if len(csv_assignment_ls_dict) == 0:
        print("no assignments")
        return
    for assignment in csv_assignment_ls_dict:
        if assignment["uuid"] and assignment["id"] == id:
            return assignment["uuid"]
    print("this assignment does not have a uuid")
    return -1


taskwarrior_tags = ["+vit", "+winsem2022"]
tag_string = " ".join(taskwarrior_tags)


def get_tw_tags():
    result = os.popen("task tags").read().split()
    result = [i for i in result if not re.match("^[0-9]+", i)][4:]
    return result


def modify_assignment_tw(uuid, field_i, modification):
    """modify_assignment_tw
    take uuid - 2
    fields that take modifications:
    - x - 3
    - name (description) - 7
    - tag (course_code) - 6
    - due - 4
    """
    task_modify_uuid_command = f"task modify {uuid} "
    if field_i == 3:
        if modification == "?":
            command = f"task stop {uuid}"
        elif modification == "-":
            command = f"task start {uuid}"
        else:
            command = f"task done {uuid}"
    elif field_i == 4:
        command = f"{task_modify_uuid_command}due:{modification}"
    elif field_i == 7:
        command = f"{task_modify_uuid_command}{uuid} description:{modification}"
    elif field_i == 6:
        tags = get_tw_tags()
        tags = [f"-{tag}" for tag in tags]
        tags = " ".join(tags)
        command = f"{task_modify_uuid_command}{tags}; {task_modify_uuid_command}{tag_string} +{modification}"
    else:
        return
    result = os.popen(command).read()
    return result


def display_assignment_dict_form_field_wise(assignment):
    """display_assignment_dict_form_field_wise
    iterate through field and print field:value for a single assignment
    """
    for i in range(1, 11):
        field_i = i % 10
        field = assignment_dict_hash[field_i]
        value = assignment[field]
        print(field, ": ", value)


def modify_assignments():
    """modify_assignments
    1. take id input
    2. choose field
    3. check input
    4. modify in tw
    5. change in dict to add to csv
    """
    display_assignments_in_csv()
    while True:
        id = input("enter id, \"exit\" when done")
        if id == "exit":
            break
        flag = 1
        # i is a single assignment in the csv
        for i in range(len(csv_assignment_modified_ls_dict)):
            if csv_assignment_modified_ls_dict[i]["uuid"] != "":
                if csv_assignment_modified_ls_dict[i]["id"] == id:
                    flag = 0
                    assignment = csv_assignment_modified_ls_dict[i]
                    csv_assignment_modified_ls_dict[i] = modify_assignment_dict(
                        assignment, tw=True)
        if flag == 1:
            print("id not found in csv, please try again")
    return


def display_all_assignments():
    """display_all_assignments
    display assignments in modified list
    """
    print("all assignments")
    display_assignment_header()
    for assignment in csv_assignment_modified_ls_dict:
        display_assignment_dict_form_tabular(assignment)
    return


def display_assignments_in_list():
    print("assignments to be added")
    display_assignment_header()
    for assignment in csv_assignment_modified_ls_dict:
        if assignment["uuid"] == "":
            display_assignment_dict_form_tabular(assignment)


def modify_assignments_in_list():
    """modify_assignments_in_list
    iterate through current list
    choose field
    change field
    """
    while True:
        display_assignments_in_list()
        id = input("enter id or exit")
        if id == "exit":
            break
        for i in range(len(csv_assignment_modified_ls_dict)):
            assignment = csv_assignment_modified_ls_dict[i]
            if assignment["id"] == id:
                new_assignment = modify_assignment_dict(assignment)
                csv_assignment_modified_ls_dict[i] = new_assignment
                break
    return


def add_assignment_to_tw(assignment):
    """ add_assignment_to_tw
    take assignment dictionary
    return the uuid of the task from taskwarrior
    """
    course_code = assignment["course"]
    course_tag = f"+{course_code}"
    due_date = assignment["due"]
    description = assignment["name"]
    tag_str = f"{tag_string} {course_tag}"
    command = f"task add {tag_str} {description} due:{due_date}"
    result = os.popen(command).read()
    if re.search("Created task", result) is not None:
        uuid_command = "task +LATEST uuids"
        result = os.popen(uuid_command).read().strip()
        return result
    return -1


def add_assignments():
    """add_assignments
    1. take assignment list
    2. iterate through assignment list
        1. create assignment
        2. add assignment to taskwarrior and get uuid
        3. add assignment to csv with uuid
    """
    assignment_write_list = []
    for i in csv_assignment_modified_ls_dict:
        if i["uuid"] == "":
            uuid_i = add_assignment_to_tw(i)
            if uuid_i == -1:
                print("error adding to taskwarrior")
                return
            i["uuid"] = uuid_i
        assignment_list = ",".join(
            [i[assignment_dict_hash[j % 10]] for j in range(1, 11)])
        assignment_write_list.append(assignment_list + '\n')
    with open(f"{assignment_dir}courses/assignments.csv", "w+") as assignments_csv:
        assignments_csv.write(
            "id,uuid,x,due,complete_by,course,name,information,links,comments\n")
        assignments_csv.writelines(assignment_write_list)
        print("assignments added")
    print("sorting csv")
    os.system(
        f"csvsort -c x,due {assignment_dir}courses/assignments.csv > {assignment_dir}courses/assignments2.csv; mv {assignment_dir}courses/assignments2.csv {assignment_dir}courses/assignments.csv")
    exit(0)


def mark_assignments_as_complete():
    """mark_assignments_as_complete
    modify list of assignments with field x and modification x
    """
    display_assignments_in_csv()
    ids = input("enter ids separated by spaces").split()
    for i in range(len(ids)):
        for j in range(len(csv_assignment_modified_ls_dict)):
            if csv_assignment_modified_ls_dict[j]["id"] == ids[i]:
                csv_assignment_modified_ls_dict[j]["x"] = "x"
                modify_assignment_tw(
                    csv_assignment_modified_ls_dict[j]["uuid"], field_i=3, modification="x")
    return


# load the assignments
assignment_list = []

os.system(f"touch {assignment_dir}courses/assignments.csv")

with open(f"{assignment_dir}courses/assignments.csv", "r+") as assignments_csv:
    _ = assignments_csv.readline()
    assignment_list = [i.strip() for i in assignments_csv.readlines()]

load_assignments(csv_assignment_list=assignment_list)

# importing from files passed to program
print("Checking for files to import")

for i in range(1, len(sys.argv)):
    file_i = sys.argv[i]
    print(f'Argument{i}: File {file_i}')
    extension = os.path.splitext(file_i)[1].lstrip(".")
    if extension == "csv":
        if os.path.exists(file_i):
            print(f"Passing {file_i} to import_from_file() function")
            import_from_file(file_i)
        else:
            error_message = f"{i}\tFile {file_i} does not exist"
            print(error_message)
            import_file_errors.append(error_message)
    else:
        error_message = f"{i}\tFile {file_i} is not a CSV"
        print(error_message)
        import_file_errors.append(error_message)

print('creating import errors file')

with open(f"{assignment_dir}assignment_import_errors.txt", "w+") as import_error_file:
    import_error_file.writelines(import_file_errors)

print("import errors saved to assignment_import_errors.txt")

# menu
while True:
    print("MENU\n")
    print("0. Display assignments in CSV")
    print("1. Display assignments to be added")
    print("2. Display original+new assignments")
    print("3. Add assignments to addition list")
    print("4. Edit assignments in list")
    print("5. Modify pre-existing assignments")
    print("6. Mark assignments as complete")
    print("7. Add assignments to tw and CSV and exit")
    print("mod 8 is used to choose elements")
    print()
    try:
        menu_choice = int(input()) % 8
    except ValueError:
        print("please enter an integer\n")
        continue
    if menu_choice == 0:
        display_assignments_in_csv()
    elif menu_choice == 1:
        display_assignments_in_list()
    elif menu_choice == 2:
        display_all_assignments()
    elif menu_choice == 3:
        add_assignment_to_list()
    elif menu_choice == 4:
        modify_assignments_in_list()
    elif menu_choice == 5:
        modify_assignments()
    elif menu_choice == 6:
        mark_assignments_as_complete()
    else:
        add_assignments()
