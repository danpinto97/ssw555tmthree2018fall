import datetime
import unittest

def get_dt_obj(string_date):
    """
    get the datetime object of a date string
    :param string_date: form of "03-MAR-1990"
    :return: datetime object
    """
    return datetime.datetime.strptime(string_date, '%d-%b-%Y')


def US36(death):
    if death == '' or death == 'N/A' or death == 'Unknown':
        #Also return true for cases where date is unknown
        return False
    death_dt = get_dt_obj(death)
    today = datetime.datetime.now()
    if today - datetime.timedelta(days=30) <= death_dt:
        return True
    return False

class TestDeath(unittest.TestCase):

    def test_2_days_ago(self):
        death = "28-SEPT-2018"
        self.assertEqual(US36(death), True)
        return

    def test_over_a_month_ago(self):
        death = "28-JAN-2018"
        self.assertEqual(US36(death), False)
        return

    def test_same_day_and_month_but_different_year(self):
        death = "28-SEPT-2016"
        self.assertEqual(US36(death), False)
        return

    def test_a_day_ago(self):
        death = "29-SEPT-2018"
        self.assertEqual(US36(death), True)
        return

    def test_today(self):
        death = "30-SEPT-2018"
        self.assertEqual(US36(death), True)
        return


