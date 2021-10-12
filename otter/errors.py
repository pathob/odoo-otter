from otter.const import FORMAT_DATETIME, FORMAT_TIME


class Error(Exception):
    def __init__(self, message):
        self.message = message


class InconsistentDataError(Error):
    def __init__(self):
        super().__init__("Data is inconsistent, check the README for options.")


class InvalidChoiceError(Error):
    def __init__(self):
        super().__init__("Invalid choice.")


class NoProjectTasksFoundError(Error):
    def __init__(self):
        super().__init__("No project tasks found, run 'otter sync' to sync them.")


class NoRecordActiveError(Error):
    def __init__(self):
        super().__init__("No active task, use 'otter start' to start a task.")


class NoRecordForDateError(Error):
    def __init__(self, date):
        super().__init__("No task found for date '{}'.".format(date))


class FormatDatetimeError(Error):
    def __init__(self, datetime):
        super().__init__("Datetime '{}' cannot be matched against format '{}' or '{}'"
                         .format(datetime, FORMAT_DATETIME, FORMAT_TIME))
