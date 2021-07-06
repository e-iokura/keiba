from data import test_db_client

def insert(data):
    db = test_db_client.get_db()
    races = db.races
    count = races.count({"race_id":data["race_id"]})
    if count == 0:
        races.insert(data)
