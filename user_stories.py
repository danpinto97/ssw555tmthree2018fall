import datetime
from dateutil.relativedelta import relativedelta

def get_dt_obj(string_date):
    """
    get the datetime object of a date string
    :param string_date: form of "03-MAR-1990"
    :return: datetime object or False in the case that the date is not known
    """
    if string_date == '' or string_date == 'N/A' or string_date == 'Unknown':
        #Also return true for cases where date is unknown
        return False
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
    today = datetime.datetime.now() + relativedelta(months=+9)
    if death > today:
        return False
    if today - datetime.timedelta(days=30) <= death:
        return True
    return False



from app import client

db = client()

def US04(family_id):
    """
    Marriage before divorce
    :param family_id:
    :return: True if marriage happened before divorce. False if not
    """
    family = db.fams.find_one({'_id': family_id})
    if family == None:
        raise ValueError('family is none')
    if family['Married'] == "":
        return True
    elif family['Divorced'] == 'N/A':
        return True
    elif get_dt_obj(family['Married']) < get_dt_obj(family['Divorced']):
        return True
    else:
        return False

def US05(family_id):
    """
    Marriage before Death
    :param family_id:
    :return: True if marriage happened before death of either spouse. False if not
    """
    family = db.fams.find_one({'_id': family_id})
    if family['Married'] == "":
        return True
    husband = db.indis.find_one({'_id': family['Husband ID']})
    wife = db.indis.find_one({'_id': family['Wife ID']})
    if husband['Death'] != 'N/A':
        if get_dt_obj(husband['Death']) < get_dt_obj(family['Married']):
            return False
    if family['Wife ID'] != 'N/A':
        if get_dt_obj(wife['Death']) < get_dt_obj(family['Married']):
            return False
    return True

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
    if birth < death:
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
    if death1 is None and death2 is None:
        return True
    if death1 is None:
        death1 = datetime.datetime.today() + 
    if death2 is None:
        return False
    if div < death1 and div < death2:
        return True
    return False


def US11(indi_id):
    """
    :param indi_id: indiviual id
    :return: True if no bigamy, false if there is
    """
    indi = db.indis.find_one({"_id": indi_id})
    spouse_list = indi["Spouse"].split()
    if len(spouse_list) <= 1:
        return True
    for marr in spouse_list:
        marr_indi = db.indis.find_one({"_id": marr})
        if marr_indi is None:
            continue
        marr_fam = db.fams.find_one({"$or": [{"$and": [{"Husband ID" : marr}, {"Wife ID": indi_id}]}, {"$and": [{"Wife ID" : marr}, {"Husband ID": indi_id}]}]})
        if marr_fam is None:
            continue
        for other_marr in spouse_list:
            if other_marr == marr:
                continue
            other_marr_indi = db.indis.find_one({"_id": other_marr})
            if other_marr_indi is None:
                continue
            other_marr_fam = db.fams.find_one({"$or": [{"$and": [{"Husband ID" : other_marr}, {"Wife ID": indi_id}]}, {"$and": [{"Wife ID" : other_marr}, {"Husband ID": indi_id}]}]})
            if other_marr_fam is None:
                continue
            if other_marr_fam["Married"]:
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

def US10(family_id):
    '''
    This function checks that a marriage does not occur before the age of 14 for all families. It does so by comparing
    the marriage date and birth dates of both Husband and Wife.
    '''
    family = db.fams.find_one({'_id':family_id})
    marriage_date = get_dt_obj(family['Married'])
    husband_birth = get_dt_obj(db.indis.find_one({'_id': family['Husband ID']})['Birthday'])
    wife_birth = get_dt_obj(db.indis.find_one({'_id': family['Wife ID']})['Birthday'])

    if husband_birth == False or wife_birth == False or marriage_date == False:
        return True

    if relativedelta(marriage_date,husband_birth).years >= 14 and relativedelta(marriage_date,wife_birth).years >= 14:
        return True
    else:
        return False

def US08(family_id):
    '''
    This function checks that a birth does not occur before the marriage date of two parents.
    Args:
         family_id: The family id to be looked up in our database to get the info needed
    Returns:
        True/False: True if the birth happens before the marriage, false otherwise.
    '''
    family = db.fams.find_one({'_id': family_id})
    marriage_date = get_dt_obj(family['Married'])
    divorce_date = get_dt_obj(family['Married'])
    if marriage_date == False or family['Children'] == 'N / A':
        return True
    children_ids = family['Children'].split()
    for _id in children_ids:
        child_birth = get_dt_obj(db.indis.find_one({'_id': _id})['Birthday'])
        if child_birth == False:
            return True
        if child_birth < marriage_date:
            print('ERROR: US08', _id, 'Birth occurs before parent\'s marriage!')
            return False
        if divorce_date is not False:
            if divorce_date.year == child_birth.year:
                if relativedelta(divorce_date,child_birth).months > 9:
                    print('ERROR: US08', _id, 'Birth occurs more than 9 months after parent\'s divorce!')
                    return False

                elif relativedelta(divorce_date,child_birth).months == 9:
                    if relativedelta(divorce_date,child_birth).days > 0:
                        print('ERROR: US08', _id, 'Birth occurs more than 9 months after parent\'s divorce!')
                        return False
    return True

def US42(date):
    try:
        spl = date.split("-")
        day = int(spl[0])
        month = int(spl[1])
        year = int(spl[2])
        test = datetime.datetime(year=year, month=month, day=day)
    except:
        return False
    else:
        return True

def US09(birth, mother_death, father_death):
    if birth is None:
        return False
    if mother_death is None and father_death is None:
        return True
    if mother_death is None:
        mother_death = datetime.datetime(year=2020, month=5, day=22)
    if father_death is None:
        father_death = datetime.datetime(year=2020, month=5, day=22)
    updated_date = father_death + relativedelta(months=+9)
    if birth < updated_date and birth < mother_death:
        return True
    return False
