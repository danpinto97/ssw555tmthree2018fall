import unittest
import app
class TestCalc(unittest.TestCase):

    def test_death_after_div(self):
        def deathAfterDivoce(div, death):
            def dateBefore(date1, date2):
                if date1 < date2:
                    return True
                return False
            if div == "N/A" or death == "N/A":
                self.assertEqual(dateBefore(div, death), False)
            else:
                self.assertEqual(dateBefore(div, death), True)

        indiv = app.indi_ids[0]
        indi = app.indis[indiv]
        fam_id = indi.getChild()
        if len(fam_id) < 1:
            fam_id = indi.getSpouse()
        fam_id = fam_id[0]
        fam = app.familes[fam_id]
        deathAfterDivoce(fam.getDivorced(), indi.getDeath())

    def test_death_after_div_2(self):
        def deathAfterDivoce(div, death):
            def dateBefore(date1, date2):
                if date1 < date2:
                    return True
                return False
            if div == "N/A" or death == "N/A":
                self.assertEqual(dateBefore(div, death), False)
            else:
                self.assertEqual(dateBefore(div, death), True)

        indiv = app.indi_ids[1]
        indi = app.indis[indiv]
        fam_id = indi.getChild()
        if len(fam_id) < 1:
            fam_id = indi.getSpouse()
        fam_id = fam_id[0]
        fam = app.familes[fam_id]
        deathAfterDivoce(fam.getDivorced(), indi.getDeath())
    
    def test_death_after_div_3(self):
        def deathAfterDivoce(div, death):
            def dateBefore(date1, date2):
                if date1 < date2:
                    return True
                return False
            if div == "N/A" or death == "N/A":
                self.assertEqual(dateBefore(div, death), False)
            else:
                self.assertEqual(dateBefore(div, death), True)

        indiv = app.indi_ids[2]
        indi = app.indis[indiv]
        fam_id = indi.getChild()
        if len(fam_id) < 1:
            fam_id = indi.getSpouse()
        fam_id = fam_id[0]
        fam = app.familes[fam_id]
        deathAfterDivoce(fam.getDivorced(), indi.getDeath())

    def test_death_after_div_4(self):
        def deathAfterDivoce(div, death):
            def dateBefore(date1, date2):
                if date1 < date2:
                    return True
                return False
            if div == "N/A" or death == "N/A":
                self.assertEqual(dateBefore(div, death), False)
            else:
                self.assertEqual(dateBefore(div, death), True)

        indiv = app.indi_ids[3]
        indi = app.indis[indiv]
        fam_id = indi.getChild()
        if len(fam_id) < 1:
            fam_id = indi.getSpouse()
        fam_id = fam_id[0]
        fam = app.familes[fam_id]
        deathAfterDivoce(fam.getDivorced(), indi.getDeath())

    def test_death_after_div_5(self):
        def deathAfterDivoce(div, death):
            def dateBefore(date1, date2):
                if date1 < date2:
                    return True
                return False
            if div == "N/A" or death == "N/A":
                self.assertEqual(dateBefore(div, death), False)
            else:
                self.assertEqual(dateBefore(div, death), True)

        indiv = app.indi_ids[4]
        indi = app.indis[indiv]
        fam_id = indi.getChild()
        if len(fam_id) < 1:
            fam_id = indi.getSpouse()
        fam_id = fam_id[0]
        fam = app.familes[fam_id]
        deathAfterDivoce(fam.getDivorced(), indi.getDeath())





