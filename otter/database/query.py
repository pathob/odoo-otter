# based on https://realpython.com/python-sqlite-sqlalchemy/#using-flat-files-for-data-storage

from datetime import date

import otter.database as database
from otter.database.model import *


def add_record(project_task_id, session=database.session(), add_date=date.today):
    record = Record(project_task_id=project_task_id, date=add_date)
    session.add(record)
    return record


def add_record_part(name, record_id, session=database.session()):
    record_track_item = RecordTrackItem(name=name, record_id=record_id)
    session.add(record_track_item)
    return record_track_item


def add_record_time_slice(record_id, time_start=datetime.now(), session=database.session()):
    record_time_slice = RecordTimeSlice(time_start=time_start, record_id=record_id)
    session.add(record_time_slice)
    return record_time_slice


def query_records_most_recent(limit, session=database.session()):
    subquery = (
        session.query(
            Record.id,
            func.max(Record.date)
        )
        .group_by(Record.project_task_id)
        .subquery()
    )

    return (
        session.query(
            Record
        )
        .join(subquery, Record.id == subquery.c.id)
        .order_by(Record.date.desc())
        .limit(limit)
        .all()
    )


def query_record_time_slice_active(session=database.session()):
    return (
        session.query(
            RecordTimeSlice
        )
        .filter(RecordTimeSlice.time_stop.is_(None))  # only unstopped
        .one()
    )

def query_record_active(session=database.session()):
    """

    :param session:
    :return:
    """
    record_time_slice = query_record_time_slice_active(session=session)
    return record_time_slice.record
