from config import db_config
from pymongo import MongoClient

def connect():
    if connect.client == None:
        connect.client = MongoClient(db_config.DB_HOST)
    return connect.client
connect.client = None

def get_db():
    client = connect()
    db = client.keiba_db
    db.authenticate(name=db_config.DB_USER_NAME, password=db_config.DB_PASSWORD)
    return db
