import datetime

def get_dt_obj(string_date):
    """
    get the datetime object of a date string
    :param string_date: form of "03-MAR-1990"
    :return: datetime object
    """
    return datetime.datetime.strptime(string_date, '%d-%b-%Y')


def US36(death):
    if death == '' or death == 'N/A' or death == 'Unknown':
        #Also return true for cases where date is unknown
        return False
    death = get_dt_obj(death)
    today = datetime.datetime.now()
    if today - datetime.timedelta(days=30) <= death:
        return True
    return False