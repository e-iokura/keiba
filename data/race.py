import test_db_client

def is_exist(race_name):
    db = test_db_client.get_db()
    race_collection = db.races
    race_count = race_collection.count({"name":race_name})
    return race_count == 1
