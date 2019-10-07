import datetime

from KortexCore.CommonUtils.Singleton import singleton
from EnumAndConsts.EnumsAndConsts import ETimeInterval


@singleton
class DateTimeHandler(object):

    time_intervals = {ETimeInterval.SECOND: 1,
                      ETimeInterval.MINUTE: 60,
                      ETimeInterval.HOUR: 3600}

    def get_default_date_time(self):
        """
        """
        start_dt = self._default_time()
        end_dt = start_dt + self._default_delta()
        return start_dt, end_dt

    def __call__(self, curr_start, start=None, end=None):
        """
        """
        if not start and not end:
            raise ValueError
        elif end and not start:
            end_dt = self.get_date_time(day=end.day, month=end.month, year=end.year,
                                        hour=end.hour, minute=end.minute)
            start_dt = curr_start
        elif start and not end:
            start_dt = self.get_date_time(day=start.day, month=start.month, year=start.year,
                                          hour=start.hour, minute=start.minute)
            end_dt = start + self._default_delta()
        else:
            start_dt = self.get_date_time(day=start.day, month=start.month, year=start.year,
                                          hour=start.hour, minute=start.minute)
            end_dt = self.get_date_time(day=end.day, month=end.month, year=end.year,
                                        hour=end.hour, minute=end.minute)

        if self.time_length(end_dt) < self.time_length(start_dt):
            raise ValueError
        return start_dt, end_dt

    def get_date_time(self, day, month, year, hour, minute):
        """
        """
        return datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)

    def date_time_from_ctime(self, datetime_str):
        """
        """
        return datetime.datetime.strptime(datetime_str, "%a %b %d %H:%M:%S %Y")

    def get_duration(self, start_dt, end_dt, time_unit):
        """
        """
        return self.time_length(end_dt, time_unit) - self.time_length(start_dt, time_unit)

    def time_length(self, dt, time_unit=ETimeInterval.MINUTE):
        """
        """
        delta = dt - datetime.datetime(1970,1,1)
        if time_unit == ETimeInterval.DAY:
            return delta.days
        return delta.total_seconds() / self.time_intervals[time_unit]

    def _default_time(self):
        """
        """
        return datetime.datetime.now()

    def _default_delta(self):
        """
        """
        return datetime.timedelta(hours=1)
