from data import test_db_client

def insert_data(data):
    db = test_db_client.get_db()
    race_results = db.race_results
    for result_data in data:
        count = race_results.count({"race_id": result_data["race_id"], "horse_id": result_data['horse_id']})
        if count == 0:
            race_results.insert(result_data)
