from datetime import date, datetime, timedelta
from otter.const import FORMAT_DATE, FORMAT_TIME, FORMAT_DATETIME


# before 5 am it's still considered last work day
from otter.errors import FormatDatetimeError


def work_date(_date=date.today()):
    if datetime.now().hour < 5:
        return _date-timedelta(days=1)
    return _date


def yesterday():
    return date.today()-timedelta(days=1)


def date_string_to_date(obj):
    if obj.upper() == "TODAY":
        return date.today()
    if obj.upper() == "YESTERDAY":
        return yesterday()
    try:
        return datetime.strptime(obj, FORMAT_DATE).date()
    except ValueError:
        raise FormatDatetimeError(obj)


def date_to_date_string(obj):
    return obj.strftime(FORMAT_DATE)


def date_to_weekday_string(obj):
    return obj.strftime('%A')


def time_string_to_datetime(obj):
    if obj.upper() == "NOW":
        return datetime.now()
    try:
        return datetime.strptime(obj, FORMAT_DATETIME)
    except ValueError:
        try:
            today = date_to_date_string(date.today())
            return datetime.strptime(f"{today} {obj}", FORMAT_DATETIME)
        except ValueError:
            raise FormatDatetimeError(obj)


# TODO: Print full date time if not same work date
def datetime_to_time_string(obj):
    return obj.strftime(FORMAT_TIME)
