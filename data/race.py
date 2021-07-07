from data import test_db_client

def insert(data):
    """
    レース情報を挿入または更新する。

    Parameters
    ----------
    data:dict
        レース情報一覧
    """
    db = test_db_client.get_db()
    races = db.races
    count = races.count({"race_id":data["race_id"]})
    if count == 0:
        races.insert(data)
    else:
        races.replace_one(filter={"race_id": data["race_id"]}, replacement=data)

def get_not_exist_data(data):
    """
    引数のレース一覧からkeiba_db.racesコレクションに既存のものを除いたレース一覧を返却する。

    Parameters
    ----------
    data:list
        レース情報一覧

    Returns
    -------
    not_exist_data:dict
        引数のレース一覧の内keiba_db.racesコレクションに存在しないレース情報一覧
    """
    db = test_db_client.get_db()
    races = db.races.find()
    return [race for race in data if races.count({"race_id":race['race_id']}) == 0]
