import datetime
from app import get_dt_obj
from app import client

db = client()


def US_11(indi_id):
    indi = db.indis.find_one({"_id": indi_id})
    if len(indi["Spouse"]) <= 1:
        return True
    for marr in indi["Spouse"].items():
        marr_indi = db.indis.find_one({"_id": marr})
        marr_fam = db.fams.find_one({"$or": [{"$and": [{"Husband ID" : marr}, {"Wife ID": indi_id}]}, {"$and": [{"Wife ID" : marr}, {"Husband ID": indi_id}]}]})
        for other_marr in indi["Spouse"].items():
            other_marr_indi = db.indis.find_one({"_id": other_mar})
            other_marr_fam = db.fams.find_one({"$or": [{"$and": [{"Husband ID" : other_marr}, {"Wife ID": indi_id}]}, {"$and": [{"Wife ID" : other_marr}, {"Husband ID": indi_id}]}]})
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
    return True

