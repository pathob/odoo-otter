# TODO: consider storing database in module data:
# import importlib.resources as resources
# with resources.path("otter.data", "otter.db") as db_path:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from otter.const import OTTER_DB


def engine():
    return create_engine(f"sqlite:///{OTTER_DB}")


def session() -> Session:
    s = sessionmaker()
    s.configure(bind=engine())
    return s()
