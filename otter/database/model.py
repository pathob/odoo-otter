# based on https://realpython.com/python-sqlite-sqlalchemy/#using-flat-files-for-data-storage
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, Boolean, Integer, Float, Date, DateTime, ForeignKey, select, func, cast
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, object_session

from otter.database import engine
# from otter.database import session as sess
from otter.util.cli import project_task_abbrev
from otter.util.date import datetime_to_time_string, date_string_to_date

Base = declarative_base()


# cached Odoo objects


# class BaseMixin(Base):
#     @classmethod
#     def create(cls, **kw):
#         obj = cls(**kw)
#         # TODO: That's so ugly
#         session = sess()
#         session.add(obj)
#         session.commit()


class Project(Base):
    __tablename__ = "project"

    odoo_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    active = Column(Boolean)
    project_tasks = relationship("ProjectTask", backref=backref("project"))

    @classmethod
    def from_odoo_json(cls, json):
        return cls(
            odoo_id=json['id'],
            name=json['name'],
            active=json['active']
        )


class ProjectTask(Base):
    __tablename__ = "project_task"

    odoo_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    active = Column(Boolean)
    project_id = Column(Integer, ForeignKey("project.odoo_id"))
    records = relationship("Record", backref=backref("project_task"))

    @classmethod
    def from_odoo_json(cls, json):
        return cls(
            odoo_id=json['id'],
            name=json['name'],
            active=json['active'],
            project_id=json['project_id'][0]
        )


class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    odoo_id = Column(Integer, unique=True)
    date = Column(Date, nullable=False)
    name = Column(String)
    unit_amount = Column(Float)
    project_task_id = Column(Integer, ForeignKey("project_task.odoo_id"))
    record_track_items = relationship("RecordTrackItem", backref=backref("record"),
                                      cascade="all, delete, delete-orphan")
    record_time_slices = relationship("RecordTimeSlice", backref=backref("record"),
                                      cascade="all, delete, delete-orphan")

    def __repr__(self):
        hh_mm = f"[{self.duration_str}]"
        return (
            f"{hh_mm} {self.project_task_abbrev(len(hh_mm)+1)}\n" +
            f"        {self.description}"
        )

    @classmethod
    def get_id_by_odoo_id(cls, odoo_id, session):
        try:
            record_id, = session.query(Record.id).filter_by(odoo_id=odoo_id).one()
            return record_id
        except NoResultFound:
            return None

    @classmethod
    def from_odoo_json(cls, local_id, json):
        return cls(
            id=local_id,
            odoo_id=json['id'],
            date=date_string_to_date(json['date']),
            name=json['name'],
            unit_amount=json['unit_amount'],
            project_task_id=json['task_id'][0]
        )

    @property
    def duration(self):
        if self.unit_amount is not None:
            return self.unit_amount
        return (
            object_session(self)
            .scalar(
                select(func.sum((
                    cast(func.coalesce(func.julianday(RecordTimeSlice.time_stop), func.julianday(datetime.now()))
                         - func.julianday(RecordTimeSlice.time_start), sqlalchemy.Float) * 24
                )))
                .where(RecordTimeSlice.record_id == self.id)
            )
        )

    @property
    def duration_str(self):
        if self.duration is not None:
            h, m = divmod(round(self.duration * 60), 60)
            return f"{h:02d}:{m:02d}"
        return None

    @property
    def description(self):
        if self.name is not None:
            return self.name
        return (
            object_session(self)
            .scalar(
                select(func.group_concat(RecordTrackItem.name, ', '))
                .where(RecordTrackItem.record_id == self.id)
            )
        )

    @property
    def project_id(self):
        return self.project_task.project_id

    @property
    def project_name(self):
        return self.project_task.project.name

    @property
    def project_task_name(self):
        return self.project_task.name

    def project_task_abbrev(self, offset_length=0):
        return project_task_abbrev(self.project_name, self.project_task_name, offset_length)

    def odoo_create_json(self):
        return {
            'date': self.date,
            'project_id': self.project_id,
            'task_id': self.project_task_id,
            'duration': self.unit_amount,
            'names': self.name
        }


# Otter objects


class RecordTrackItem(Base):
    __tablename__ = "record_track_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    record_id = Column(Integer, ForeignKey("record.id"), nullable=False)


class RecordTimeSlice(Base):
    __tablename__ = "record_time_slice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # the start time may never be null while the stop time is null until it the work got stopped
    time_start = Column(DateTime, nullable=False)
    time_stop = Column(DateTime, nullable=True)
    record_id = Column(Integer, ForeignKey("record.id"), nullable=False)

    @property
    def time_start_str(self):
        return datetime_to_time_string(self.time_start)

    @property
    def time_stop_str(self):
        return datetime_to_time_string(self.time_stop)


Base.metadata.create_all(engine())
