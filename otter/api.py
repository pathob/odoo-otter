from datetime import datetime

from sqlalchemy.exc import NoResultFound

import otter.database.query as db
from otter import database
from otter.database.model import Project, ProjectTask, Record
from otter.model import OtterRecordSyncCalculator
from otter.odoo import rest
from otter.util.date import work_date


def get_or_create_record(project_task_id):
    """
    :param project_task_id: project task ID
    :return: record
    """

    current_date = work_date()
    session = database.session()

    try:
        return (
            session.query(
                Record
            )
            .filter(Record.date == current_date)
            .filter(Record.project_task_id == project_task_id)
            .filter(Record.odoo_id.is_(None))  # only unsynced
            .one()
        )
    except NoResultFound:
        record = db.add_record(project_task_id, session=session, add_date=current_date)
        session.commit()
        session.refresh(record)
        return record


def get_records(query_date, session=database.session()):
    return (
        session.query(
            Record
        )
        .filter(Record.date == query_date)
        .all()
    )


def sync_remote_projects(session=database.session()):
    projects_json = rest.get_projects_json()
    if projects_json is not None:
        for project_json in projects_json:
            session.merge(Project.from_odoo_json(project_json))
    session.commit()


def sync_remote_project_tasks(session=database.session()):
    project_tasks_json = rest.get_project_tasks_json()
    if project_tasks_json is not None:
        for task_json in project_tasks_json:
            session.merge(ProjectTask.from_odoo_json(task_json))
    session.commit()


def sync_local_records(query_date, session=database.session()):
    records = []  # get_records_until_date(date=query_date, only_unsynced=True, session)

    if len(records) > 0:
        record_sync_calc = OtterRecordSyncCalculator(records)

        for i, day in enumerate(record_sync_calc.dates()):
            # print() if i > 0 else None
            # print(f"{date_to_weekday_string(day)}, {date_to_date_string(day)}:")
            sync_records = record_sync_calc.records(day)

            for sync_record in sync_records:
                assert sync_record.odoo_id is None

                if sync_record.duration == 0:
                    session.delete(sync_record)
                    session.commit()
                    continue

                record_odoo_id = rest.post_record(sync_record.odoo_create_json())
                assert record_odoo_id is not None
                sync_record.odoo_id = record_odoo_id
                session.commit()


def sync_remote_records(session=database.session()):
    record_json = rest.get_records_json()
    if record_json is not None:
        for record_json in record_json:
            local_id = Record.get_id_by_odoo_id(record_json['id'], session)
            session.merge(Record.from_odoo_json(local_id, record_json))
    session.commit()
