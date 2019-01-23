import datetime


def get_previous_date(days):
    today = datetime.date.today()
    daynums = datetime.timedelta(days=days)
    previousday = today-daynums
    return previousday