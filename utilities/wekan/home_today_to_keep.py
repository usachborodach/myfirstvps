from pymongo import MongoClient
import pyperclip
import webbrowser

MONGO_ADDRESS = '172.29.1.9'
MONGO_PORT = 27017
HOME_TODAY_LIST_ID = 'cph83ZAWgRkSbWD3o'

def main():
    client, db = connect_to_mongo()
    cards_to_clipboard(db)
    open_keep()
    client.close()

def open_keep():
    keep_url = 'https://keep.google.com/#NOTE/'
    note_id = '1633qtJidoxeD5UFPEG1P5Axk2iTn7h_fb_3DtmuDQAupvdHWNtKlsGRbxfigB8Kk'
    webbrowser.open(keep_url + note_id)

def cards_to_clipboard(db):
    collection = db['cards']
    query = {'listId': HOME_TODAY_LIST_ID, 'archived': False}
    projection = {'_id': 0, 'title': 1, 'sort': 1}
    cursor = collection.find(query, projection).sort('sort', 1)
    docs = list(cursor)
    res = str()
    for doc in docs:
        res += doc['title'] + '\n'
    pyperclip.copy(res)

def connect_to_mongo():
    client = MongoClient(f'mongodb://{MONGO_ADDRESS}:{MONGO_PORT}/')
    db = client['wekan']
    return client, db

if __name__ == "__main__":
    main()