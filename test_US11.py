import unittest
import app
import pymongo

db = app.client()


class TestClass(unittest.TestCase):

    def test_person1(self):
        person1_id = db.indis.find_one({})["_id"]
        self.assertEqual(app.no_bigamy(person1_id), True)
        return

    def test_person2(self):
        person2_id = db.indis.find_one({})["_id"]
        self.assertEqual(app.no_bigamy(person2_id), True)
        return

    def test_person3(self):
        person3_id = db.indis.find_one({})["_id"]
        self.assertEqual(app.no_bigamy(person3_id), True)
        return

    def test_person4(self):
        person4_id = db.indis.find_one({})["_id"]
        self.assertEqual(app.no_bigamy(person4_id), True)
        return

    def test_person5(self):
        person5_id = db.indis.find_one({})["_id"]
        self.assertEqual(app.no_bigamy(person5_id), True)
        return

if __name__ == '__main__':
    unittest.main()