import unittest
import app
import user_stories
import datetime
from user_stories import *
db = client()
current_date = datetime.datetime.now()

class TestUS01(unittest.TestCase):
    def test_year_plus_10(self):
        ten_years_later = current_date + datetime.timedelta(days=3650)
        # adding 10 years (3650 days) should return false as it is a future date
        self.assertEqual(US01(
            str(current_date.day) + '-' + current_date.strftime("%B").upper()[0:3] + '-' + str(ten_years_later.year)),
                         False)
        return

    def test_tomorrow(self):
        tomorrow = current_date + datetime.timedelta(days=1)
        # adding 1 day should return false as it is a future date
        self.assertEqual(US01(
            str(tomorrow.day) + '-' + tomorrow.strftime("%B").upper()[0:3] + '-' + str(current_date.year)), False)
        return

    def test_today(self):
        # today should return true as it is possible
        self.assertEqual(US01(
            str(current_date.day) + '-' + current_date.strftime("%B").upper()[0:3] + '-' + str(current_date.year)),
                         True)
        return

    def test_month_plus_1(self):
        # 1 month later returns false because it is in the future
        one_month_later = current_date + datetime.timedelta(days=31)
        # adding 31 will increase by 1 month AT LEAST
        self.assertEqual(US01(
            str(current_date.day) + '-' + one_month_later.strftime("%B").upper()[0:3] + '-' + str(current_date.year)),
                         False)
        return

    def test_old_date(self):
        # for now we check just a past date. since it will always be in the past and will not change as time goes on we don't need to use datetime for this one4
        self.assertEqual(US01('1-JAN-1950'), True)
        return


class TestUS07(unittest.TestCase):
    def test_greater_than_150_years(self):
        self.assertEqual(US07('1-JAN-1700', '1-JAN-1950'), True)
        return

    def test_less_than_150_years(self):
        self.assertEqual(US07('1-JAN-1700', '1-JAN-1790'), False)
        return

    def test_150_years_minus_one_day(self):
        self.assertEqual(US07('5-JAN-1700', '4-JAN-1850'), False)
        return

    def test_150_years_plus_day(self):
        self.assertEqual(US07('5-JAN-1700', '6-JAN-1850'), True)
        return

    def test_150_years_minus_month(self):
        self.assertEqual(US07('5-MAR-1700', '5-FEB-1850'), False)
        return

    def test_150_years(self):
        self.assertEqual(US07('5-MAR-1700', '5-MAR-1850'), False)
        return

class TestUS11(unittest.TestCase):

    def test_person1(self):
        person1_id = db.indis.find_one({})["_id"]
        self.assertEqual(user_stories.US11(person1_id), True)
        return

    def test_person2(self):
        person2_id = db.indis.find_one({})["_id"]
        self.assertEqual(user_stories.US11(person2_id), True)
        return

    def test_person3(self):
        person3_id = db.indis.find_one({})["_id"]
        self.assertEqual(user_stories.US11(person3_id), True)
        return

    def test_person4(self):
        person4_id = db.indis.find_one({})["_id"]
        self.assertEqual(user_stories.US11(person4_id), True)
        return

    def test_person5(self):
        person5_id = db.indis.find_one({})["_id"]
        self.assertEqual(user_stories.US11(person5_id), True)
        return

class TestUS36(unittest.TestCase):

    def test_2_days_ago(self):
        tomorrow = current_date - datetime.timedelta(days=2)
        self.assertEqual(US36(tomorrow), True)
        return

    def test_over_a_month_ago(self):
        death = current_date - datetime.timedelta(days=32)
        self.assertEqual(US36(death), False)
        return

    def test_year_ago(self):
        death = current_date - datetime.timedelta(days=365)
        self.assertEqual(US36(death), False)
        return

    def test_tomorrow(self):
        death = current_date + datetime.timedelta(days=1)
        self.assertEqual(US36(death), False)
        return

    def test_today(self):
        self.assertEqual(US36(current_date), True)
        return


class TestUS02(unittest.TestCase):
    def test_two_unknowns(self):
        self.assertEqual(US02(None, None), True)
        return
    def test_left_unk(self):
        #15 Sept 2001
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US02(None, test), True)
        return
    def test_right_unk(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US02(test, None), True)
        return
    def test_proper(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US02(birth, marriage), True)
        return
    def test_reversed(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US02(marriage, birth), False)
        return

class TestUS03(unittest.TestCase):
    def test_two_unknowns(self):
        self.assertEqual(US03(None, None), True)
        return
    def test_left_unk(self):
        #15 Sept 2001
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US03(None, test), True)
        return
    def test_right_unk(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US03(test, None), True)
        return
    def test_proper(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US03(birth, marriage), True)
        return
    def test_reversed(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US03(marriage, birth), False)
        return

class TestUS06(unittest.TestCase):
    def test_nones(self):
        self.assertEqual(US06(None, None, None), False)
        return
    def test_some_nones(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US06(None, None, test), False)
        return
    def test_more_nones(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US06(None, test, None), False)
        return
    def test_proper(self):
        self.assertEqual(US06('8-JUN-1920', '5-MAR-2001', '7-AUG-2001'), False)
        return
    def test_improper(self):
        self.assertEqual(US06('5-MAR-2001', '8-JUN-1920', '7-AUG-2001'), True)
        return



class TestUS37(unittest.TestCase):

    def test_person1(self):
        dead_indi = db.indis.find_one({"_id": "@I2@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I2@"), test_survivors)
        return

    def test_person2(self):
        dead_indi = db.indis.find_one({"_id": "@I7@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I7@"), test_survivors)
        return

    def test_person3(self):
        dead_indi = db.indis.find_one({"_id": "@I10@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I10@"), test_survivors)
        return

    def test_person4(self):
        dead_indi = db.indis.find_one({"_id": "@I19@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I19@"), test_survivors)
        return

    def test_person5(self):
        dead_indi = db.indis.find_one({"_id": "@I28@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I28@"), test_survivors)
        return

class TestUS04(unittest.TestCase):

    def test_person1(self):
        test_1 = db.fams.find_one()
        self.assertEqual(US04(test_1['_id']), True)
        return

    def test_person2(self):
        test_2 = db.fams.find_one({})
        self.assertEqual(US04(test_2['_id']), True)
        return

    def test_person3(self):
        test_3 = db.fams.find_one({})
        self.assertEqual(US04(test_3['_id']), True)
        return

    def test_person4(self):
        test_4 = db.fams.find_one({})
        self.assertEqual(US04(test_4['_id']), True)
        return

    def test_person5(self):
        test_5 = db.fams.find_one({})
        self.assertEqual(US04(test_5['_id']), True)
        return


class TestUS05(unittest.TestCase):
    def test_person1(self):
        test_1 = db.fams.find_one({})
        self.assertEqual(US05(test_1['_id']), True)
        return

    def test_person2(self):
        test_2 = db.fams.find_one({})
        self.assertEqual(US05(test_2['_id']), True)
        return

    def test_person3(self):
        test_3 = db.fams.find_one({})
        self.assertEqual(US05(test_3['_id']), True)
        return

    def test_person4(self):
        test_4 = db.fams.find_one({})
        self.assertEqual(US05(test_4['_id']), True)
        return

    def test_person5(self):
        test_5 = db.fams.find_one({})
        self.assertEqual(US05(test_5['_id']), True)
        return

class TestUS08(unittest.TestCase):
    def test_false(self):
        self.assertEqual(US08('@F9@'), False)
    def test_true(self):
        self.assertEqual(US08('@F4@'), True)

class TestUS10(unittest.TestCase):
    def test_false(self):
        self.assertEqual(US10('@F5@'), True)
    def test_true(self):
        self.assertEqual(US10('@F5@'), True)

class TestUS42(unittest.TestCase):
    def test_date_1(self):
        self.assertEqual(US42("04-DEC-1998"), True)
    def test_date_2(self):
        self.assertEqual(US42("07-13-1995"), False)
    def test_date_3(self):
        self.assertEqual(US42("14-22-1964"), False)
    def test_date_4(self):
        self.assertEqual(US42("45-12-1973"), False)
    def test_date_5(self):
        self.assertEqual(US42("ABC"), False)

class TestUS09(unittest.TestCase):
    def test_date_1(self):
        self.assertEqual(US09(None, None, None), False)
    def test_date_2(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US09(test, None, None), True)
    def test_date_3(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        mom = datetime.datetime(2007, 9, 15, 0, 0)
        dad = datetime.datetime(2003, 9, 15, 0, 0)
        #mom and dad death dates > birthdate should be true
        self.assertEqual(US09(test, mom, dad), True)
    def test_date_4(self):
        test = datetime.datetime(2008, 9, 15, 0, 0)
        mom = datetime.datetime(2007, 9, 15, 0, 0)
        dad = datetime.datetime(2003, 9, 15, 0, 0)
        self.assertEqual(US09(test, mom, dad), False)
    def test_date_5(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        dad = datetime.datetime(2005, 7, 13, 0, 0)
        self.assertEqual(US09(test, None, dad), True)

class TestUS12(unittest.TestCase):
    test_families = []
    for family in db.fams.find().limit(5):
        test_families.append(family['_id'])
    def test_person1(self):
        test_1 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[0]), True)
        return

    def test_person2(self):
        test_2 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[1]), True)
        return

    def test_person3(self):
        test_3 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[2]), True)
        return

    def test_person4(self):
        test_4 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[3]), False)
        return

    def test_person5(self):
        test_5 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[4]), True)
        return

class TestUS14(unittest.TestCase):
    test_families = []
    for family in db.fams.find().limit(5):
        test_families.append(family['_id'])
    def test_person1(self):
        test_1 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[0]), True)
        return

    def test_person2(self):
        test_2 = db.fams.find_one({})
        self.assertEqual(US05(self.test_families[1]), True)
        return

class TestUS25(unittest.TestCase):
    def test_fam_with_duplicate(self):
        self.assertEqual(US25('@F16@'), True)
    def test_fam_no_duplicates(self):
        self.assertEqual(US25('@F4@'), False)

class TestUS29(unittest.TestCase):
    def test_na(self):
        #Alive is false but no death date is present
        self.assertEqual(US29('False','N/A'), False)
    def test_unknown(self):
        #Alive is true should always return False
        self.assertEqual(US29('True','Unknown'), False)
    def test_real_date(self):
        #Alive is false and death date is present
        self.assertEqual(US29('False','8-MAR-2018'), True)

class TestUS22(unittest.TestCase):
    def test_all_unique(self):
        indivs = []
        for i in range(0, 10):
            indiv = {
                '_id': '@I'+str(i)+'@',
                'name': 'Place Holder',
                'birth': '01 JAN 1998'
            }
            indivs.append(indiv)
        self.assertEqual(US22(indivs), True)

    def test_all_not_unique(self):
        indivs = []
        temp = {'_id': '@I7@', 'name': 'Duplicate Id', 'birth': '01 APR 2018'}
        indivs.append(temp)
        for i in range(0, 10):
            indiv = {
                '_id': '@I'+str(i)+'@',
                'name': 'Place Holder',
                'birth': '01 JAN 1998'
            }
            indivs.append(indiv)
        self.assertEqual(US22(indivs), False)

class TestUS23(unittest.TestCase):
    def test_all_not_unique(self):
        indivs = []
        indiv1 = {
                    '_id': '@I1@',
                    'name': 'Place Holder',
                    'birth': '01 JAN 1998'
                }
        indiv2 = {
                    '_id': '@I2@',
                    'name': 'Place Holder',
                    'birth': '01 JAN 1998'
                }
        indivs.extend([indiv1, indiv2])
        self.assertEqual(US23(indivs), False)
    def test_all_unique(self):
        indivs = []
        indiv1 = {
                    '_id': '@I1@',
                    'name': 'Place Holder-ORIG',
                    'birth': '01 JAN 1998'
                }
        indiv2 = {
                    '_id': '@I2@',
                    'name': 'Place Holder',
                    'birth': '01 JAN 1998'
                }
        indivs.extend([indiv1, indiv2])
        self.assertEqual(US23(indivs), True)
class TestUS21(unittest.TestCase):
    def test_correct(self):
        fam = {'wife': {'Gender': 'F'}, 'husband': {'Gender': 'M'}}
        self.assertEqual(US21(fam), True)
    def test_incorrect(self):
        fam = {'wife': {'Gender': 'F'}, 'husband': {'Gender': 'F'}}
        self.assertEqual(US21(fam), False)
class TestUS30(unittest.TestCase):
    def test_living_married(self):
        fam = {'stuff': {'divorce': 'N/A', 'marriage': '01 JAN 1990'}, 'wife': {'Alive': 'True'}, 'husband': {'Alive': 'True'}}
        self.assertEqual(US30(fam), True)
    def test_not_living_married(self):
        fam = {'stuff': {'divorce': 'N/A', 'marriage': '01 JAN 1990'}, 'wife': {'Alive': 'False'}, 'husband': {'Alive': 'True'}}
        self.assertEqual(US30(fam), False)
if __name__ == '__main__':
    unittest.main()
