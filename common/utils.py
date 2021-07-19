import pytz
from datetime import datetime

### Support Functions
def total_seconds_datetime(time):
    """
    Receives datetime instance and returns int total seconds  
    :param datetime: datetime instance
    :return int
    """
    if isinstance(time, datetime):
        return time.second + time.minute * 60 + time.hour * 3600
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_bissextile(today):
    """
    Check if the year is bissextile
    """
    if (today.year % 4 == 0 and today.year % 100 != 0) or (today.year % 400 == 0):
        return True
    return False


### validations 
def is_startmonth(today):
    """
    Check if today is startmonth day
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if today.day == 1:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_endmonth(today):
    """
    Check if today is endmonth day
    :param today: datetime instance current day
    :return boolean
    """

    if isinstance(today, datetime):

        # check 30 days months
        if (
            today.month == 11
            or today.month == 4
            or today.month == 6
            or today.month == 9
        ):
            if today.day == 30:
                return True
            return False

        # check 31 days months
        if (
            today.month == 1
            or today.month == 3
            or today.month == 5
            or today.month == 7
            or today.month == 8
            or today.month == 10
            or today.month == 12
        ):
            if today.day == 31:
                return True
            return False

        # check february month
        if is_bissextile(today):
            last_february_day = 29
        else:
            last_february_day = 28

        if today.day == last_february_day:
            return True
        return False

    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_starttrimester(today):
    """
    Check if today is starttrimester day
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if today.day == 1 and today.month == 1:
            return True
        elif today.day == 1 and today.month == 4:
            return True
        elif today.day == 1 and today.month == 7:
            return True
        elif today.day == 1 and today.month == 10:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_endtrimester(today):
    """
    Check if today is endtrimester day
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if today.day == 31 and today.month == 1:
            return True
        elif today.day == 30 and today.month == 4:
            return True
        elif today.day == 31 and today.month == 7:
            return True
        elif today.day == 31 and today.month == 10:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_startyear(today):
    """
    Check if today is startyear day
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if today.day == 1 and today.month == 1:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_endyear(today):
    """
    Check if today is endyear day
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if today.day == 31 and today.month == 12:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_dayofnewtrimester(day, today):
    """
    Check if today is specific day of new trimester
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if today.day == int(day) and today.month == 1:
            return True
        elif today.day == int(day) and today.month == 4:
            return True
        elif today.day == int(day) and today.month == 7:
            return True
        elif today.day == int(day) and today.month == 10:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_dayofweek(day, today):
    """
    Check if today is specific day of week
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        int_day = int(day)
        if today.weekday() == int_day - 1:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_dayofmonth(day, today):
    """
    Check if today is specific day of month
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        int_day = int(day)
        if today.day == int_day:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_once(today, last_send):
    """
    Check if the last send was in the same day, if yes return False
    :param today: datetime instance current day
    :return boolean
    """
    if isinstance(today, datetime):
        if last_send is not None:
            if today.date() != last_send.date():
                return True
            return False
        return True
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_between(start, end, now):
    """
    Check if now is valid time for send news
    :param start: str represents the hour of begin 
    :param end: str represents the end of time
    :param last_send: datetime represents the last send of this newsletter
    :return boolean
    """
    now_today = now
    start_hour = start.split(":")
    end_hour = end.split(":")
    end_hour = now.replace(
        hour=int(end_hour[0]), minute=int(end_hour[1])#, second=int(end_hour[2])
    )
    start_hour = now.replace(
        hour=int(start_hour[0]), minute=int(start_hour[1])#, second=int(start_hour[2])
    )

    if now_today >= start_hour and now_today <= end_hour:
        return True
    return False


def is_oncebetween(start, end, last_send, now):
    """
    Check if now is valid time for send news, if last_send is between the range of hours returns False
    :param start: str represents the hour of begin 
    :param end: str represents the end of time
    :param last_send: datetime represents the last send of this newsletter
    :return boolean
    """

    if last_send is not None:
        now_today = now
        start_hour = start.split(":")
        end_hour = end.split(":")
        end_hour = now_today.replace(
            hour=int(end_hour[0]), minute=int(end_hour[1]), second=int(end_hour[2])
        )
        start_hour = now_today.replace(
            hour=int(start_hour[0]), minute=int(start_hour[1]), second=int(start_hour[2])
        )

        if now_today >= start_hour and now_today <= end_hour:
            if last_send >= start_hour and last_send <= end_hour:
                return False
        return True
    return True


def is_intervalhours(total_hours, last_send, now):
    """
    Check if the hour is in the valid interval of hours 
    :param total_hours: str total hours value 
    :param last_send: datetime last send
    :param now: datetime now
    :return boolean
    """
    now_today = now
    now_today = now_today.replace(
        hour=int(total_hours.split(":")[0]),
        minute=int(total_hours.split(":")[1])
    )

    if isinstance(now, datetime):
        if last_send is not None:
            total_time_passed = now - last_send
            if total_time_passed.total_seconds() > total_seconds_datetime(now_today):
                return True
            return False
        return True
    else:
        raise Exception("{} or {}  is not a datetime instance".format(last_send, today))


def is_monthname(day, month, today):
    """
    Check if today is specific day of specific month 
    :param 
    :param today: datetime instance current day
    :return boolean
    """
    int_month = 0

    if month == "january":
        int_month = 1
    elif month == "february":
        int_month = 2
    elif month == "march":
        int_month = 3
    elif month == "april":
        int_month = 4
    elif month == "may":
        int_month = 5
    elif month == "june":
        int_month = 6
    elif month == "july":
        int_month = 7
    elif month == "august":
        int_month = 8
    elif month == "september":
        int_month = 9
    elif month == "october":
        int_month = 10
    elif month == "november":
        int_month = 11
    elif month == "december":
        int_month = 12

    if isinstance(today, datetime):
        int_day = int(day)
        if today.day == int_day and today.month == int_month:
            return True
        return False
    else:
        raise Exception("{}  is not a datetime instance".format(today))


def is_intervalbusinesshours(total_hours, last_send, now):
    """
    Check if the hour is in the valid interval of hours 
    :param total_hours: str total hours value 
    :param last_send: datetime last send
    :param now: datetime now
    :param holiday_list: list with day and month 
    :return boolean
    """

    now_today = now
    now_today = now_today.replace(
        hour=int(total_hours.split(":")[0]),
        minute=int(total_hours.split(":")[1])
    )

    if isinstance(now, datetime):
        if last_send is not None:
            total_time_passed = now - last_send
            if total_time_passed.total_seconds() > total_seconds_datetime(now_today) and now_today.weekday() != 6 and now_today.weekday() != 0:
                return True
            return False
        return True
    else:
        raise Exception("{} or {}  is not a datetime instance".format(last_send, today))