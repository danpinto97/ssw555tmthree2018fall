import datetime
from dateutil.relativedelta import relativedelta

from pymongo import MongoClient

def client():
    """
    Connects to the mongoDB client
    """
    client = MongoClient('localhost',27017)
    return client.ged
db = client()
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
    date = get_dt_obj(date)
    if date == False:
        return True
    if datetime.datetime.now() > date:
        return True
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
    birth = get_dt_obj(birth)
    if birth == False:
        return False
    death = get_dt_obj(death)
    if death is False and relativedelta(datetime.datetime.now(),birth).years > 150:
        return True
    if relativedelta(datetime.datetime.now(), birth).years == 150 and relativedelta(datetime.datetime.now(), birth).days > 1:
            return True
    if death == False:
        return False

    difference_years = relativedelta(death,birth).years
    difference_days = relativedelta(death,birth).days
    if difference_years > 150:
        return True
    elif difference_years == 150 and difference_days > 0:
        #If it is exactly 150 years we need to check edge case if it is 1 or more days into the future
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

def US04(family_id):
    """
    Marriage before divorce
    :param family_id:
    :return: True if marriage happened before divorce. False if not
    """
    family = db.fams.find_one({'_id': family_id})
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
    if wife['Death'] != 'N/A':
        if get_dt_obj(wife['Death']) < get_dt_obj(family['Married']):
            return False
    return True

def US03(birth, death):
    '''
    This function checks for birth before death
    Args:
        birth: date taken in as datetime to be tested.
        death: date taken in as datetime to be tested.
    Returns:
        True/False: True if the birth comes before the death date, False if not.
        Should always be true in case of birth or death not known.
    '''
    if type(birth) == str and type(death) == str:
        birth = get_dt_obj(birth)
        death = get_dt_obj(death)
    if birth is False or birth is None:
        return True
    if death is False or death is None:
        return True
    if birth < death:
        return True
    return False

def US02(birth, marriage):
    '''
    This function checks for birth before marriage
    Args:
        birth: date taken in as datetime to be tested.
        marriage: date taken in as datetime to be tested.
    Returns:
        True/False: True if the birth comes before the marriage date, False if not.
    '''
    if type(birth) == str and type(marriage) == str:
        birth = get_dt_obj(birth)
        marriage = get_dt_obj(marriage)
    if birth is False or birth is None:
        return True
    if marriage is False or marriage is None:
        return True
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
            try:
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
            except:
                continue
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
    '''
    This function tests whether a date format is acceptable or not.
    Args:
        date: takes in a date in the form of a string
    Returns:
        True/False: True if date is acceptable format, False otherwise.
    '''
    try:
        spl = date.split("-")
        day = int(spl[0])
        month = int(spl[1])
        year = int(spl[2])
        test = datetime.datetime(year=year, month=month, day=day)
    except:
        return False
    return True

def US09(birth, mother_death, father_death):
    '''
    This function checks for a birth before the death of parents.
    Args:
        birth: birthdate of child
        mother_death: deathdate of mother
        father_death: deathdate of father
    Returns:
        True/False: True if birth is before death of both parents (or death of father + 9 months for pregnancy), else False
    '''
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
