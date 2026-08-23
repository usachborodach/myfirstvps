import common
from datetime import datetime

def main():
    today_str = get_today_str()
    token = common.get_token()
    # common.post_card(today_str, 'work', token)
    client, db = common.connect_to_mongo()
    min_sort_val = get_min_sort_val(db)
    print(min_sort_val)

def get_min_sort_val(db):
    collection = db['cards']
    list_id = common.get_list_id(db, 'work', 'Дейлик')
    query = {'archived': False, 'listId': list_id}
    projection = {'_id': -1, 'sort':1}
    cursor = collection.find(query, projection).sort('sort', 1).limit(1)
    docs = list(docs)
    return docs[0]['sort']

def get_today_str():
    today = datetime.today()
    return datetime.strftime(today, '%d.%m')

if __name__ == '__main__':
    main()