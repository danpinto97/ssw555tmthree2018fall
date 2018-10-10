import datetime
#git push --force-with-lease origin
from family import Family
from individual import Individual
from pymongo import MongoClient
from prettytable import PrettyTable
def client():
    """
    Connects to the mongoDB client
    """
    client = MongoClient('localhost',27017)
    return client.ged
db = client()
indis = db.indis
fams = db.fams

#Calculate Age via birthdate
def calculate_age(birth_date):
    today = datetime.datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def main():
    #Initialize Dictionaries for family and individuals
    familes = {}
    indis = {}
    #Need Arrays for IDs to iterate through list (?) might be wrong, it works right now, but could save on space complexity
    fam_ids = []
    indi_ids = []
    current = False #False -> indi // True -> Family
    working = False #true after the first individual or family has been read
    #If DEAT, BIRT, MARR, DIV flag is raised, see if next line is a date.
    looking_date_birth = False
    looking_date_death = False
    looking_date_marr = False
    looking_date_div = False
    current_id = ""
    #read file one line at a time from file in open(...)
    with open("test_family.ged") as f:
        for line in f:
            line = line.strip('\n')
            #dont work with empty lies
            if len(line.rstrip()) > 1:
                #comments not wanted
                if line[0] is not "#":
                    #splits input string at every space to seperate everything out
                    spl = line.split()
                    tag = ""
                    num = spl[0]
                    if(len(spl) > 2):
                        if(spl[2]=="INDI" or spl[2]=="FAM") and (spl[1] !="INDI" or spl[1]!="FAM"):
                            #if tag is INDI or FAM then all lines after will add to this class until another tag is found in
                            #which the previous class is stored

                            if working:
                                if current:
                                    familes[current_id] = temp
                                    fam_ids.append(current_id)
                                    temp = None
                                else:
                                    indis[current_id] = temp
                                    indi_ids.append(current_id)
                                    temp = None
                            current_id = spl[1]
                            working = True
                            tag = spl[2]
                            if tag == "INDI":
                                temp = Individual(spl[1])
                                current = False
                            else:
                                temp = Family(spl[1])
                                current = True

                        else: #get tag
                            tag=spl[1]
                    else: #get tag
                        tag = spl[1]
                    args = ""
                    for i in range(2, len(spl)):
                        args = args + spl[i]
                    if num == "1":
                        #check for wanted tags
                        looking_date_birth = False
                        looking_date_death = False
                        looking_date_marr = False
                        looking_date_div = False
                        if tag == "NAME":
                            temp.setName(args)
                        if tag == "SEX":
                            temp.setGender(spl[2])
                        if tag == "BIRT":
                            looking_date_birth = True
                        if tag == "DEAT":
                            temp.setAlive(False)
                            looking_date_death = True
                        if tag == "FAMC":
                            temp.addChild(spl[2])
                        if tag == "FAMS":
                            temp.addSpouse(spl[2])
                        if tag == "MARR":
                            looking_date_marr = True
                        if tag == "HUSB":
                            temp.setHusbandID(spl[2])
                            husb = indis[spl[2]]
                            husb_name = husb.getName()
                            temp.setHusbandName(husb_name)
                        if tag == "WIFE":
                            temp.setWifeID(spl[2])
                            wife = indis[spl[2]]
                            wife_name = wife.getName()
                            temp.setWifeName(wife_name)
                        if tag == "CHIL":
                            temp.addChild(spl[2])
                        if tag == "DIV":
                            looking_date_div = True
                    elif num == "2":
                        #if num is a 2, check for DATE tag, if so see if the most recent line was a MARR, DIV, DEAT, OR BIRT
                        #if yes add
                        if tag == "DATE":
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
                            if len(spl) == 3:
                                date=spl[2]
                                dt = datetime.datetime(year=int(spl[2]), month=1, day=1)
                            if len(spl) == 4:
                                date=spl[2] + "-" + spl[3]
                                dt = datetime.datetime(year=int(spl[3]), month=date_int[spl[2]], day=1)
                            if len(spl) == 5:
                                date=spl[2] + "-" + spl[3] + "-" + spl[4]
                                dt = datetime.datetime(year=int(spl[4]), month=date_int[spl[3]], day=int(spl[2]))
                            if looking_date_birth:
                                temp.setBirthday(date)
                                age = calculate_age(dt)
                                temp.setAge(age)
                            if looking_date_death:
                                temp.setDeath(date)
                            if looking_date_div:
                                temp.setDivorced(date)
                            if looking_date_marr:
                                temp.setMarried(date)

                        looking_date_birth = False
                        looking_date_death = False
                        looking_date_marr = False
                        looking_date_div = False
                    else: #ensure last element added
                        if tag == "TRLR":
                            if working:
                                if current:
                                    familes[current_id] = temp
                                    fam_ids.append(current_id)
                                    temp = None
                                else:
                                    indis[current_id] = temp
                                    indi_ids.append(current_id)
                                    temp = None
                        looking_date_birth = False
                        looking_date_death = False
                        looking_date_marr = False
                        looking_date_div = False
    #Printing information->Individuals first, then families
    #Pretty table wouldnt install on my machine, but if one of yall can get it feel free, but dont delete this stuff bc if i need to go back and test
    #i dont want to re-write this portion
    individual_table = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    family_table = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    indi_ptable = PrettyTable(individual_table)
    print("Individuals: ")

    for indiv in indi_ids:
        indi = indis[indiv]
        children_temp = indi.getChild()
        spouses_temp = indi.getSpouse()
        children_temp_str = ' '.join(children_temp)
        spouses_temp_str = ' '.join(spouses_temp)
        individual_table_info = [indi.getID(), indi.getName(), indi.getGender(), indi.getBirthday(),
                                 str(indi.getAge()), str(indi.getAlive()), indi.getDeath(), children_temp_str,
                                 spouses_temp_str]
        current_id = ''
        current_list_for_ptable= []
        for i in range(0, len(individual_table)):
            if individual_table[i] == "ID":
                current_id = individual_table_info[i]
                # if table[i] is ID, we need to set it to current id and insert just the the _id as the correlating ID to the db.
            db.indis.find_one_and_update({"_id": current_id},
                                         {'$set': {individual_table[i]: individual_table_info[i]}}, upsert=True)
            # now we find that _id and continue to update it with whatever info we have until we reach a new ID and then
            # repeat with that ID
            current_list_for_ptable.append(individual_table_info[i])
            if individual_table[i] == "Spouse":
                indi_ptable.add_row(current_list_for_ptable)
                current_list_for_ptable.clear()
    print(indi_ptable)

    fam_ptable = PrettyTable(family_table)
    current_list_for_ptable = []
    print("\nFamilies: ")
    for family_id in fam_ids:
        family = familes[family_id]
        children_temp = family.getChild()
        child_str = ' '.join(children_temp)
        family_table_info = [family.getID(), family.getMarried(), family.getDivorced(), family.getHusbandID(),
                             family.getHusbandName(), family.getWifeID(), family.getWifeName(), child_str]
        current_id = ''
        for i in range(0, len(family_table)):
            if family_table[i] == "ID":
                current_id = family_table_info[i]

            db.fams.find_one_and_update({"_id": current_id}, {'$set': {family_table[i]: family_table_info[i]}},
                                        upsert=True)
            current_list_for_ptable.append(family_table_info[i])
            if family_table[i] == "Children":
                fam_ptable.add_row(current_list_for_ptable)
                current_list_for_ptable.clear()
    print(fam_ptable)

    from user_stories import US36, US01, US07
    recent_survivor_ids = []
    for item in db.indis.aggregate([
        {'$match': {'Birthday': {'$exists': True}, 'Death' : {'$exists': True}}},
        {'$project' : {
            'dates':{'birth':'$Birthday', 'death': '$Death'}}}
    ]):
        if US07(item['dates']['birth'],item['dates']['death']):
            print('ERROR: Person older than 150 years!')
        if US01(item['dates']['birth']) == False or US01(item['dates']['death']) == False:
            print('ERROR: Past current date!')
        if US36(item['dates']['death']):
            recent_survivor_ids.append(item['_id'])

    if len(recent_survivor_ids) > 0:
        print('Recent survivor ids: ',recent_survivor_ids)

    for item in db.fams.aggregate([
        {'$match': {'Married': {'$exists': True}, 'Divorced': {'$exists': True}}},
        {'$project': {
            'dates': {'divorce': '$Married', 'marriage': '$Divorced'}}}
    ]):
        if US01(item['dates']['divorce']) == False or US01(item['dates']['marriage']) == False:
            print('ERROR: Past current date!')

if __name__ == '__main__':
    main()