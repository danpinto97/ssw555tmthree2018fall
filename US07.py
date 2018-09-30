def us07_death(birth, death):
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

'''
from US07 import us07_death

for item in db.indis.aggregate([
    {'$match': {'Birthday': {'$exists': True}, 'Death' : {'$exists': True}}},
    {'$project' : {
        'dates':{'birth':'$Birthday', 'death': '$Death'}}}
]):
    print(us07_death(item['dates']['birth'],item['dates']['death']))
'''
