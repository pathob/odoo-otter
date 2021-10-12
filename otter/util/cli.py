import getpass
import os
import sys

from otter import const, eprint


def input_auth(args):
    username = args.username
    password = args.password

    if username is None:
        username = input("Username: ")
    if args.username is None or password is None:
        password = getpass.getpass(prompt='Password: ', stream=None)

    return username, password


def input_confirm(args):
    if args.batch:
        return True
    return input_yes_no('Are you sure to continue?')


def input_yes_no(message, default='n'):
    choices = 'Y/n' if default.lower() == 'y' else 'y/N'
    while True:
        choice = input(f"{message} [{choices}]]: ").strip().lower()
        if choice not in ('', 'y', 'n'):
            continue
        if choice == '':
            choice = default
        return choice == 'y'


def input_default(key, default=None):
    if default is not None:
        choice = input("{} [{}]: ".format(key, default))
        return choice if choice != "" else default
    return input("{}: ".format(key))


def input_select_list_default(key, list, default=None):
    if list is None or len(list) == 0:
        return None

    if default is not None:
        print(f"{key} [{default}]:")
    else:
        print(f"{key}:")

    for i, item in enumerate(list):
        print(f"{i + 1}: {item}")

    choice = input("?: ")
    if default is not None:
        choice = choice if choice != "" else default
        if choice == default:
            return default

    return list[int(choice)-1]

def print_task_start(message):
    print(message, end=' ', flush=True)


def print_task_done(message="Done."):
    print(message)


def print_progress(title, percentage):
    sys.stdout.write("\r%s: %d%%" % (title, percentage))
    sys.stdout.flush()
    if percentage == 100:
        print()


def project_task_abbrev(project, task, offset_len=0):
    column_len = os.get_terminal_size().columns
    extra_len = offset_len + len(const.SEPARATOR)
    project_len = len(project)
    task_len = len(task)

    min_width = extra_len + 16 # 16 is min length for project + task

    # Require minimum 8 chars for both project and task
    if column_len < min_width: 
        eprint(f"Terminal too small, minimum width is {min_width} columns.")
        sys.exit(1)

    common_len = project_len + task_len
    target_len = min(common_len, column_len-extra_len)

    project_part = round(target_len * (float(project_len) / float(common_len)))
    task_part = target_len - project_part

    if project_len > project_part:
        project_list = list(project[:project_part])
        project_list[project_part-1] = const.DOTS
        project = ''.join(project_list)

    if task_len > task_part:
        task_list = list(task[:task_part])
        task_list[task_part-1] = const.DOTS
        task = ''.join(task_list)

    return f"{project}{const.SEPARATOR}{task}"
