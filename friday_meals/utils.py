from datetime import datetime


CURRENT_WEEK = datetime.now().isocalendar()[1]


def get_current_week():
    return datetime.now().isocalendar()[1]


def get_current_date():
    return datetime.now()
