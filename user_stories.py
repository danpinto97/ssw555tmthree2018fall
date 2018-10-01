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


from app import client

db = client()


def US11(indi_id):
    indi = db.indis.find_one({"_id": indi_id})
    spouse_list = indi["Spouse"].split()
    if len(spouse_list) <= 1:
        return True
    for marr in spouse_list:
        marr_indi = db.indis.find_one({"_id": marr})
        marr_fam = db.fams.find_one({"$or": [{"$and": [{"Husband ID" : marr}, {"Wife ID": indi_id}]}, {"$and": [{"Wife ID" : marr}, {"Husband ID": indi_id}]}]})
        for other_marr in spouse_list:
            if other_marr == marr:
                continue
            other_marr_indi = db.indis.find_one({"_id": other_marr})
            other_marr_fam = db.fams.find_one({"$or": [{"$and": [{"Husband ID" : other_marr}, {"Wife ID": indi_id}]}, {"$and": [{"Wife ID" : other_marr}, {"Husband ID": indi_id}]}]})
            if get_dt_obj(other_marr_fam["Married"]) < get_dt_obj(marr_fam["Married"]):
                if other_marr_fam["Divorced"]:
                    if get_dt_obj(other_marr_fam["Divorced"]) > get_dt_obj(marr_fam["Married"]):
                        return False
                elif other_marr_indi["death"] != "N/A":
                    if get_dt_obj(other_marr_indi["death"]) > get_dt_obj(marr_fam["Married"]):
                        return False
                else:
                    return False
            elif get_dt_obj(other_marr_fam["Married"]) > get_dt_obj(marr_fam["Married"]):
                if marr_fam["Divorced"]:
                    if get_dt_obj(marr_fam["Divorced"]) > get_dt_obj(other_marr_fam["Married"]):
                        return False
                elif marr_indi["death"] != "N/A":
                    if get_dt_obj(marr_indi["death"]) > get_dt_obj(other_marr_fam["Married"]):
                        return False
                else:
                    return False
    return True

def US37(recent_dead_id):
    dead_indi = db.indis.find_one({"_id": recent_dead_id})
    survivors = []
    spouse_list = dead_indi["Spouse"].split()
    child_list = dead_indi["Child"].split()
    if len(spouse_list) > 0:
        for spouse in spouse_list:
            survivors.append(spouse)
    if len(child_list) > 0:
        for child in child_list:
            survivors.append(child)
    return survivors

