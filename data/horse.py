from data import test_db_client

def get_not_exist_ids(horse_ids):
    """
    引数の競走馬ID一覧からDBに存在しないID一覧を抽出して返却する。

    Parameters
    ----------
    horse_ids:list of str
        競走馬IDリスト

    Returns
    -------
    not_exist_ids:list of str
        DBに存在しない競走馬IDリスト
    """
    db = test_db_client.get_db()
    horses = [horse['horse_id'] for horse in db.horses.find()]
    return [horse_id for horse_id in horse_ids if horse_id not in horses]

def insert(data):
    """
    競走馬情報を挿入する。

    Parameters
    ----------
    data:list of dict
        競走馬データ一覧
    """
    db = test_db_client.get_db()
    horses = db.horses
    for horse in data:
        count = horses.count({"horse_id":horse['horse_id']})
        if count == 0:
            horses.insert(horse)
        else:
            horses.replace_one(filter={"horse_id":horse['horse_id']},replacement=horse)
