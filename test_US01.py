import datetime
import unittest

import us01

current_date = datetime.datetime.now()
class TestApp(unittest.TestCase):

    def test_year_plus_10(self):
        ten_years_later = current_date + datetime.timedelta(days= 3650)
        # adding 10 years (3650 days) should return false as it is a future date
        self.assertEqual(us01.check_date_vs_datetimenow(str(current_date.day)+'-'+current_date.strftime("%B").upper()[0:3]+'-'+str(ten_years_later.year)), False)
        return

    def test_tomorrow(self):
        tomorrow = current_date+ datetime.timedelta(days=1)
        #adding 1 day should return false as it is a future date
        self.assertEqual(us01.check_date_vs_datetimenow(str(tomorrow.day)+'-'+current_date.strftime("%B").upper()[0:3]+'-'+str(current_date.year)), False)
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

if __name__ == '__main__':
    unittest.main()