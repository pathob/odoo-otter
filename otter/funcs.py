from otter.api import *
from otter.config import *
from otter.database.query import *
from otter.errors import *
from otter.odoo import rest
from otter.util.cli import *
from otter.util.date import *


# logging.basicConfig(
#     level=logging.INFO,
#     # format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         logging.StreamHandler(sys.stdout)
#     ]
# )
# import validators
# or https://stackoverflow.com/a/7160778/4278102


def choose_project_task_id(args):
    limit = 9  # maybe from config

    records = query_records_most_recent(limit)

    if len(records) == 0:
        raise NoProjectTasksFoundError()

    # print("0: Search")
    for i, record in enumerate(records):
        print(f"{i + 1}: {record.project_task_abbrev(3)}")

    choice = int(input("?: "))

    if choice > limit:
        raise InvalidChoiceError()

    project_task_id = None

    if choice > 0:
        project_task_id = records[choice - 1].project_task_id

    # else:
    #     input("Project: ")
    #     input("Task: ")

    assert project_task_id is not None
    return project_task_id


def start(args):
    session = database.session()
    time_start = time_string_to_datetime(args.time)
    project_task_id = choose_project_task_id(args)
    record = get_or_create_record(project_task_id)

    try:
        # eiter stop it or use it
        record_time_slice = query_record_time_slice_active(session=session)

        # TODO: If date is not work date, ask user to stop it first

        # does running task matches selected one?
        if record_time_slice.record.project_task_id == project_task_id:
            print("Work on project task '{}' is already running since {}"
                  .format(record_time_slice.record.project_task_abbrev(),
                          record_time_slice.time_start_str))
            sys.exit(0)

        # if not, stop old one... TODO: Reuse stop here
        record_time_slice.time_stop = time_start
        session.commit()

        print("Stopped work on project task '{}' at {}"
              .format(record_time_slice.record.project_task_abbrev(),
                      record_time_slice.time_stop_str))

    except NoResultFound:
        pass

    # logging.info(f"Create new otter_record_time_slice's")
    record_time_slice = add_record_time_slice(record.id, time_start=time_start, session=session)
    session.commit()
    session.flush(record_time_slice)

    print("Started work on project task '{}' at {}"
          .format(record_time_slice.record.project_task_abbrev(),
                  record_time_slice.time_start_str))


def stop(args):
    session = database.session()
    time_stop = time_string_to_datetime(args.time)

    try:
        record_time_slice = query_record_time_slice_active(session=session)
        record_time_slice.time_stop = time_stop
        session.commit()

        print("Stopped work on project task '{}' at {}"
              .format(record_time_slice.record.project_task_abbrev(),
                      record_time_slice.time_stop_str))

    except NoResultFound:
        raise NoRecordActiveError()


def describe(args):
    session = database.session()
    description = args.description

    try:
        record_time_slice = query_record_time_slice_active(session=session)
        add_record_part(description, record_time_slice.record_id, session)
        session.commit()

        print("Tracked work '{}' for task '{}'"
              .format(description, record_time_slice.record.project_task_abbrev()))

    except NoResultFound:
        raise NoRecordActiveError()


def show(args):
    # Also offer finding by weekdays, see https://stackoverflow.com/q/319426/4278102
    session = database.session()
    query_date = work_date(date_string_to_date(args.date))
    records = get_records(query_date, session=session)

    if len(records) == 0:
        raise NoRecordForDateError(args.date)

    overall_duration = 0.0

    print("{}, {}:"
          .format(date_to_weekday_string(query_date),
                  date_to_date_string(query_date)))

    for record in records:
        overall_duration += record.duration
        print()
        print(record)

    h, m = divmod(round(overall_duration * 60), 60)

    print()
    print(f"[{h:02d}:{m:02d}] Overall")


def status(args):
    try:
        record = query_record_active()

        print("Active task:")
        print()
        print(record)

    except NoResultFound:
        raise NoRecordActiveError()


def sync(args):
    # Maybe transform into flag '--include-today'
    query_date = date_string_to_date(args.date)

    print("Syncing remote Odoo projects...", end=' ')
    sync_remote_projects()
    print("Done.")

    print("Syncing remote Odoo project tasks...", end=' ')
    sync_remote_project_tasks()
    print("Done.")

    print("Syncing local Otter records...", end=' ')
    sync_local_records(query_date)
    print("Done.")

    print("Syncing remote Odoo records...", end=' ')
    sync_remote_records()
    print("Done.")


def login(args):
    cfg = deserialize()

    url = input_default("URL", cfg['url'] if 'url' in cfg else None)
    url = url.rstrip('/')
    cfg['url'] = url
    serialize(cfg)

    # if not validators.url(url):
    #     sys.exit(1)

    databases = rest.get_databases_json(url)
    odoo_db = input_select_list_default("Database", databases, cfg['db'] if 'db' in cfg else None)
    cfg['db'] = odoo_db
    serialize(cfg)

    username = input_default("Username", cfg['user'] if 'user' in cfg else None)
    cfg['user'] = username
    serialize(cfg)

    password = args.password
    session = cfg['session'] if 'session' in cfg else None

    # TODO: Check if session still active
    # if session is not None:
    #     print("Already logged in as user '" + username + "'")
    #     sys.exit(0)

    if password is None:
        password = getpass.getpass(prompt='Password: ', stream=None)

    (uid, session) = rest.login(url, odoo_db, username, password)

    # # Contains all info like cookie expiry date
    # # Convert key-value String to dictionary using dict() + generator expression + split() + map()
    # auth_cookies = dict(map(str.strip, auth_cookie.split('=', 1)) \
    #     for auth_cookie in login_response.headers['set-cookie'].split('; ') if '=' in auth_cookie)

    cfg['uid'] = uid
    cfg['session'] = session
    serialize(cfg)
    print("Successfully logged in")


def logout(args):
    cfg = deserialize()
    user = cfg['user'] if 'user' in cfg else None
    if 'session' in cfg:
        del cfg['session']
        serialize(cfg)
        print("Successfully logged out as user '" + user + "'")
    else:
        print("Already logged out")
