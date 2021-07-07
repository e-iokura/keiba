from data import test_db_client

def insert_data(data):
    """
    レース結果情報をkeiba_db.race_resultsコレクションに挿入、または更新する

    Parameters
    data:dict
        レース結果情報一覧
    """
    db = test_db_client.get_db()
    race_results = db.race_results
    for result_data in data:
        count = race_results.count({"race_id": result_data["race_id"], "horse_id": result_data['horse_id']})
        if count == 0:
            race_results.insert(result_data)
        else:
            race_results.replace_one(filter={"race_id": result_data["race_id"], "horse_id": result_data['horse_id']},replacement=result_data)
