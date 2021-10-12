from otter.util.math import ceil_duration, float_mod, round_duration, floor_duration


class OtterRecordSyncCalculator(object):

    def __init__(self, records=None):
        self.records_by_date = {}
        if records is None:
            records = []
        self.add_records(records)

    def add_record(self, record):
        if record.date not in self.records_by_date:
            self.records_by_date[record.date] = []
        self.records_by_date[record.date].append(record)

    def add_records(self, records):
        for record in records:
            self.add_record(record)

    def dates(self):
        return self.records_by_date.keys()

    def target_duration(self, date):
        """
        Calculate the overall duration of all records of a day (date)
        and round up the result to the next 15 minutes (0.25 in decimal).
        E.g. a duration of 7.83 will be rounded up to 8.0.
        """

        duration_hours = 0.0
        for record in self.records_by_date[date]:
            duration_hours += record.duration
        return ceil_duration(duration_hours)

    def records(self, date):
        """
        Get the records of a day (date) with re-calculated durations.
        """

        records = []

        # this is the target value to reach
        target_duration_hours = self.target_duration(date)

        # the sum of all rounded records can be lower or higher than the target value,
        # this is what we are going to fix here
        duration_hours_records_rounded = 0.0
        for record in self.records_by_date[date]:
            duration_hours_records_rounded += round_duration(record.duration)

        # a negative difference means that the summed up rounded durations
        # result in too high overall duration, we need to reduce it
        difference = target_duration_hours - duration_hours_records_rounded

        # how many times we have to fix the rounded value?
        times = int(abs(difference // 0.25))
        mod_record_tuples = []

        for record in self.records_by_date[date]:
            mod = float_mod(record.duration * 4.0) / 4.0
            mod_record_tuples.append((mod, record))

        increase = difference > 0
        mod_record_tuples.sort(key=lambda tup: tup[0], reverse=increase)

        for mod, record in mod_record_tuples:
            target_duration_hours = round_duration(record.duration)
            ceiled = record.duration < target_duration_hours

            if times > 0:
                if increase and not ceiled:
                    target_duration_hours = ceil_duration(record.duration_hours())
                    times = times - 1
                elif not increase and ceiled:
                    target_duration_hours = floor_duration(record.duration_hours())
                    times = times - 1

            record.unit_amount = target_duration_hours
            records.append(record)

        return records
