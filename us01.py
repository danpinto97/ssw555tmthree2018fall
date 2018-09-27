import datetime

def check_date_vs_datetimenow(date):
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
