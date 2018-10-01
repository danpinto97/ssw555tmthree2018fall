import unittest
import app
db = app.client()
import datetime
from user_stories import US01, US36, US07, US13, US15, US06, US37
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

class TestUS13(unittest.TestCase):
    def test_two_unknowns(self):
        self.assertEqual(US13(None, None), False)
        return
    def test_left_unk(self):
        #15 Sept 2001
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US13(None, test), False)
        return
    def test_right_unk(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US13(test, None), False)
        return
    def test_proper(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US13(birth, marriage), True)
        return
    def test_reversed(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US13(marriage, birth), False)
        return

class TestUS15(unittest.TestCase):
    def test_two_unknowns(self):
        self.assertEqual(US15(None, None), False)
        return
    def test_left_unk(self):
        #15 Sept 2001
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US15(None, test), False)
        return
    def test_right_unk(self):
        test = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US15(test, None), False)
        return
    def test_proper(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US15(birth, marriage), True)
        return
    def test_reversed(self):
        birth = datetime.datetime(1920, 8, 4, 0, 0)
        marriage = datetime.datetime(2001, 9, 15, 0, 0)
        self.assertEqual(US15(marriage, birth), False)
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
        div = datetime.datetime(1920, 8, 4, 0, 0)
        death1 = datetime.datetime(2001, 9, 15, 0, 0)
        death2 = datetime.datetime(2001, 9, 17, 0, 0)
        self.assertEqual(US06(div, death1, death2), True)
        return
    def test_improper(self):
        div = datetime.datetime(1920, 8, 4, 0, 0)
        death1 = datetime.datetime(2001, 9, 15, 0, 0)
        death2 = datetime.datetime(2001, 9, 17, 0, 0)
        self.assertEqual(US06(death1, div, death2), False)
        return


class TestUS37(unittest.TestCase):

    def test_person1(self):
        dead_indi = db.indis.find_one({"_id": "@I6000000081764934924@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I6000000081764934924@"), test_survivors)
        return

    def test_person2(self):
        dead_indi = db.indis.find_one({"_id": "@I6000000081764947910@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I6000000081764947910@"), test_survivors)
        return

    def test_person3(self):
        dead_indi = db.indis.find_one({"_id": "@I6000000081765016854@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I6000000081765016854@"), test_survivors)
        return

    def test_person4(self):
        dead_indi = db.indis.find_one({"_id": "@I6000000081764012539@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I6000000081764012539@"), test_survivors)
        return

    def test_person5(self):
        dead_indi = db.indis.find_one({"_id": "@I6000000081765037935@"})
        test_survivors = []
        spouse_list = dead_indi["Spouse"].split()
        child_list = dead_indi["Child"].split()
        if len(spouse_list) > 0:
            for spouse in spouse_list:
                test_survivors.append(spouse)
        if len(child_list) > 0:
            for child in child_list:
                test_survivors.append(child)

        self.assertEqual(US37("@I6000000081765037935@"), test_survivors)
        return

if __name__ == '__main__':
    unittest.main()