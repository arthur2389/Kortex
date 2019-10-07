import datetime

from KortexCore.CommonUtils.Singleton import singleton
from EnumAndConsts.EnumsAndConsts import ETimeInterval


@singleton
class DateTimeHandler(object):

    minute_to_time_unit = {ETimeInterval.MINUTE: 1,
                           ETimeInterval.HOUR: 60,
                           ETimeInterval.DAY: 1440}

    def __init__(self):
        pass

    def get_default_date_time(self):
        """
        """
        start_dt = self._default()
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

        if int(end_dt) < int(start_dt):
            raise ValueError
        return start_dt, end_dt

    def get_date_time(self, day, month, year, hour, minute):
        """
        """
        return datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)

    def date_time_from_str(self, datetime_str):
        date, time = datetime_str.split(" ")
        day, month, year = self._parse_date(date)
        hour, minute = self._parse_time(time)
        return self.get_date_time(day=day, month=month, year=year, hour=hour, minute=minute)

    def get_duration(self, start_dt, end_dt, time_unit):
        duration = self.time_length(end_dt) - self.time_length(start_dt)
        return float(duration/self.minute_to_time_unit[time_unit])

    def time_length(self, dt):
        return int(dt)

    def _default_time(self):
        return datetime.datetime.now()

    def _default_delta(self):
        return datetime.timedelta(hours=1)

    def _parse_date(self, date_str):
        """
        Turns "DD:MM:YYYY" to integers that represent the date
        param dateStr: "DD:MM:YYYY" (str)
        return: day, month, year (tuple (int, int, int))
        """
        data_list = date_str.split("/")
        if len(data_list) != 3:
            raise TypeError
        return int(data_list[0]), int(data_list[1]), int(data_list[2])

    def _parse_time(self, time_str):
        """
        Turns "HH:MM" to integers that represent the time
        param dateStr: "HH:MM" (str)
        return: hours, minutes (tuple (int, int))
        """
        data_list = time_str.split(":")
        if len(data_list) != 2:
            raise TypeError
        return int(data_list[0]), int(data_list[1])
