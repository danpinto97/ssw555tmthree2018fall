import datetime
import unittest

import us01
from US07 import us07_death
current_date = datetime.datetime.now()
print(current_date)
class TestUS01(unittest.TestCase):
    def test_year_plus_10(self):
        ten_years_later = current_date + datetime.timedelta(days= 3650)
        # adding 10 years (3650 days) should return false as it is a future date
        self.assertEqual(us01.check_date_vs_datetimenow(str(current_date.day)+'-'+current_date.strftime("%B").upper()[0:3]+'-'+str(ten_years_later.year)), False)
        return

    def test_tomorrow(self):
        tomorrow = current_date+ datetime.timedelta(days=1)
        #adding 1 day should return false as it is a future date
        self.assertEqual(us01.check_date_vs_datetimenow(str(tomorrow.day)+'-'+tomorrow.strftime("%B").upper()[0:3]+'-'+str(current_date.year)), False)
        return

    def test_today(self):
        #today should return true as it is possible
        self.assertEqual(us01.check_date_vs_datetimenow(str(current_date.day)+'-'+current_date.strftime("%B").upper()[0:3]+'-'+str(current_date.year)), True)
        return

    def test_month_plus_1(self):
        #1 month later returns false because it is in the future
        one_month_later = current_date+ datetime.timedelta(days=31)
        #adding 31 will increase by 1 month AT LEAST
        self.assertEqual(us01.check_date_vs_datetimenow(str(current_date.day)+'-'+one_month_later.strftime("%B").upper()[0:3]+'-'+str(current_date.year)), False)
        return

    def test_old_date(self):
        #for now we check just a past date. since it will always be in the past and will not change as time goes on we don't need to use datetime for this one4
        self.assertEqual(us01.check_date_vs_datetimenow('1-JAN-1950'), True)
        return

class TestUS07(unittest.TestCase):
    def test_greater_than_150_years(self):
        self.assertEqual(us07_death('1-JAN-1700','1-JAN-1950'),True)
        return
    def test_less_than_150_years(self):
        self.assertEqual(us07_death('1-JAN-1700','1-JAN-1790'),False)
        return
    def test_150_years_minus_one_day(self):
        self.assertEqual(us07_death('5-JAN-1700','4-JAN-1850'),False)
        return
    def test_150_years_plus_day(self):
        self.assertEqual(us07_death('5-JAN-1700','6-JAN-1850'),True)
        return
    def test_150_years_minus_month(self):
        self.assertEqual(us07_death('5-MAR-1700', '5-FEB-1850'), False)
        return

if __name__ == '__main__':
    unittest.main()