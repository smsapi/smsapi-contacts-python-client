# -*- coding: utf-8 -*-


from datetime import datetime, timedelta, tzinfo
from .compat import text_type

date_format = "%Y-%m-%d"

iso8601_datetime_format = '%Y-%m-%dT%H:%M:%S%z'


class FixedOffset(tzinfo):

    def __init__(self, offset_hours=0, offset_minutes=0, name="UTC"):
        super(FixedOffset, self).__init__()

        self.__offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return timedelta(0)


def convert_to_utf8_str(data):
    """
    Convert data to string.
    """

    if isinstance(data, text_type):
        data = data.encode('utf-8')
    elif not isinstance(data, str):
        data = str(data)
    return data


def convert_iso8601_str_to_datetime(iso8601_str):
    """
    Convert date string in iso8601 format to datetime object.
    """

    date_str, utc_time_str = iso8601_str.split('T')
    time_str, utc_offset = utc_time_str[:8], utc_time_str[-6:]

    date = date_str.split('-')
    time = time_str.split(':')
    utc_offset = utc_offset.replace(':', '')[1:]

    utc_offset_hours, utc_offset_minutes = utc_offset[:2], utc_offset[2:]

    fixed_offset = FixedOffset(int(utc_offset_hours), int(utc_offset_minutes))

    return datetime(int(date[0]), int(date[1]), int(date[2]),
                    int(time[0]), int(time[1]), int(time[2]),
                    tzinfo=fixed_offset)


def convert_date_str_to_date(date_str):
    """
    Convert date string to date object.
    """

    return datetime.strptime(date_str, date_format).date()


def is_http_success(status_code):
    """
    Check if status code belongs to class of http success codes (2xx).

    Return:
        True if status code is succes, False otherwise.
    """

    return not int(str(status_code)[:2]) != 20