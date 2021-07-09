from data import test_db_client

def insert_dates(data):
    """
    keiba_db.datesコレクションに未登録の開催データを挿入する

    Returns
    -------
    insert_data:list of dict
        新規で挿入した開催データ一覧
    """
    db = test_db_client.get_db()
    dates = db.dates
    insert_data = []
    for kaisai_date in data:
        count = dates.count({"kaisai_id": kaisai_date["kaisai_id"],"course_name":kaisai_date['course_name']})
        if count == 0:
            dates.insert(kaisai_date)
            insert_data.append(kaisai_date)

    return insert_data

def get_dates():
    """
    keiba_db.datesコレクション全件取得。

    Returns
    -------
    dates:list of dict
        開催データ一覧
    """
    db = test_db_client.get_db()
    return db.dates.find()