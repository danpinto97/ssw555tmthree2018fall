import datetime

def get_dt_obj(string_date):
    """
    get the datetime object of a date string
    :param string_date: form of "03-MAR-1990"
    :return: datetime object
    """
    return datetime.datetime.strptime(string_date, '%d-%b-%Y')

def US01(date):
    '''
    Function to check if dates (birth, marriage, divorce, death) are after the current date. If so, returns error.
    Args:
        date- a date from individual/family_table_info to be checked with today's date
    Returns:
        True/False- if false returns, this means that the date is after the current date
    '''
    if date == '' or date == 'N/A' or date == 'Unknown':
        #Also return true for cases where date is unknown
        return True

    date_int = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }

    today = datetime.datetime.now()
    date = date.split('-')
    #convert from abbreviation back to number using date_int[date[1]]
    if today.year > eval(date[2]):
        return True
    elif today.year < eval(date[2]):
        return False
    elif today.year ==  eval(date[2]):
        if today.month > date_int[date[1]]:
            return True
        elif today.month == date_int[date[1]]:
            if today.day < eval(date[0]):
                return False
            else:
                return True
        else:
            return False

def US07(birth, death):
    '''
    This function checks if a person has been alive for more than 150 years. It does so by comparing the birth and death
    dates passed to it.
    Args:
        Birth: String that contains a birth date from the gedcom file
        Death: String that contains a death date from the gedcom file
    Returns:
        True/False: True if the person has been alive for more than 150 years, otherwise False.
    '''
    if birth == '' or birth == 'N/A' or birth == 'Unknown':
        # Also return true for cases where date is unknown
        return False
    if death == '' or death == 'N/A' or death == 'Unknown':
        # Also return true for cases where date is unknown
        return False
    date_int = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }
    birth = birth.split('-')
    death = death.split('-')

    if eval(death[2]) - eval(birth[2]) > 150:
        #i.e. if 2011 - 1990 > 150
        return True
    elif eval(death[2]) - eval(birth[2]) == 150:
        #i.e. if 2011 - 1990 > 150
        if date_int[death[1]] > date_int[birth[1]]:
            return True
        elif date_int[death[1]] == date_int[birth[1]]:
            if death[0] > birth[0]:
                return True
    return False

def US36(death):
    '''
     This function checks all deaths in the past 30 days.
     Args:
        death: date taken in as string or datetime to be tested. This should be a death from the gedcom file.
    Returns:
        True/False: True if the death has occurred within the past 30 days, False if not.
    '''

    if death == '' or death == 'N/A' or death == 'Unknown':
        #Also return true for cases where date is unknown
        return False
    if type(death) is  str:
        death = get_dt_obj(death)
    today = datetime.datetime.now()
    if death > today:
        return False
    if today - datetime.timedelta(days=30) <= death:
        return True
    return False

def US13(birth, death):
    '''
    This function checks for birth before death
    Args:
        birth: date taken in as datetime to be tested.
        death: date taken in as datetime to be tested.
    Returns:
        True/False: True if the birth comes before the death date, False if not.
    '''
    if birth is None:
        return False
    if death is None:
        return False
    if birth < date:
        return True
    return False

def US15(birth, marriage):
    '''
    This function checks for birth before marriage
    Args:
        birth: date taken in as datetime to be tested.
        marriage: date taken in as datetime to be tested.
    Returns:
        True/False: True if the birth comes before the marriage date, False if not.
    '''
    if birth is None:
        return False
    if marriage is None:
        return False
    if birth < marriage:
        return True
    return False

def US06(div, death1, death2):
    '''
    This function checks for divorce before deaths of both spouses
    Args:
        div: Divorce date
        death1: death date
        death2: partner death date
    Returns:
        True/False: True if the divorce comes before death, False if not.
    '''
    if div is None:
        return False
    if death1 is None:
        return False
    if death2 is None:
        return False
    if div < death1 and div < death2:
        return True
    return False