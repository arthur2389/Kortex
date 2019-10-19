import datetime

from KortexCore.Exception.Exception import *
from EnumAndConsts.EnumsAndConsts import ETimeInterval


class DateTimeHandler(object):

    time_intervals = {ETimeInterval.SECOND: 1,
                      ETimeInterval.MINUTE: 60,
                      ETimeInterval.HOUR: 3600}

    @staticmethod
    def get_default_date_time():
        """
        """
        start_dt = DateTimeHandler._default_time()
        end_dt = start_dt + DateTimeHandler._default_delta()
        return start_dt, end_dt

    @staticmethod
    def start_and_end_time(curr_start, start=None, end=None):
        """
        """
        if not start and not end:
            raise BadInput
        elif end and not start:
            end_dt = DateTimeHandler.get_date_time(day=end.day, month=end.month, year=end.year,
                                                   hour=end.hour, minute=end.minute)
            start_dt = curr_start
        elif start and not end:
            start_dt = DateTimeHandler.get_date_time(day=start.day, month=start.month, year=start.year,
                                                     hour=start.hour, minute=start.minute)
            end_dt = start_dt + DateTimeHandler._default_delta()
        else:
            start_dt = DateTimeHandler.get_date_time(day=start.day, month=start.month, year=start.year,
                                                     hour=start.hour, minute=start.minute)
            end_dt = DateTimeHandler.get_date_time(day=end.day, month=end.month, year=end.year,
                                                   hour=end.hour, minute=end.minute)

        return start_dt, end_dt

    @staticmethod
    def get_date_time(day, month, year, hour, minute):
        """
        """
        return datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)

    @staticmethod
    def date_time_from_ctime(datetime_str):
        """
        """
        return datetime.datetime.strptime(datetime_str, "%a %b %d %H:%M:%S %Y")

    @staticmethod
    def validate(start_dt, end_dt):
        if start_dt and end_dt:
            start_dt = DateTimeHandler.get_date_time(day=start_dt.day, month=start_dt.month, year=start_dt.year,
                                                     hour=start_dt.hour, minute=start_dt.minute)
            end_dt = DateTimeHandler.get_date_time(day=end_dt.day, month=end_dt.month, year=end_dt.year,
                                                   hour=end_dt.hour, minute=end_dt.minute)
            if DateTimeHandler.time_length(end_dt) < DateTimeHandler.time_length(start_dt):
                raise BadDateTime
        if end_dt and not start_dt:
            raise BadDateTime

    @staticmethod
    def get_duration(start_dt, end_dt, time_unit):
        """
        """
        return DateTimeHandler.time_length(end_dt, time_unit) - DateTimeHandler.time_length(start_dt, time_unit)

    @staticmethod
    def time_length(dt, time_unit=ETimeInterval.MINUTE):
        """
        """
        delta = dt - datetime.datetime(1970, 1, 1)
        if time_unit == ETimeInterval.DAY:
            return delta.days
        return delta.total_seconds() / DateTimeHandler.time_intervals[time_unit]

    @staticmethod
    def _default_time():
        """
        """
        return datetime.datetime.now()

    @staticmethod
    def _default_delta():
        """
        """
        return datetime.timedelta(hours=1)
