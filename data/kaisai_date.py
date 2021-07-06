from data import test_db_client

def insert_dates(data):
    db = test_db_client.get_db()
    collection = db.dates
    for kaisai_date in data:
        count = collection.count({"kaisai_id": kaisai_date["kaisai_id"],"course_name":kaisai_date['course_name']})
        if count == 0:
            collection.insert(kaisai_date)
