import common
from datetime import datetime

def main():
    today_str = get_today_str()
    token = common.get_token()

    response = common.post_card(today_str, 'work', 'Новые', token)
    print(response)
    exit()


    client, db = common.connect_to_mongo()
    list_id = common.get_list_id('work', 'Дейлик')
    min_sort_val = get_min_sort_val(db, list_id)
    set_sort_val(min_sort_val, today_str, db, list_id)
    client.close()

def set_sort_val(min_sort_val, today_str, db, list_id):
    collection = db['cards']
    query = {'listId':list_id, 'title': today_str}
    decr_sort_val = min_sort_val - 1
    collection.update_one(query, {'$set': {'sort': decr_sort_val}})

    doc = collection.find_one(query)
    print(doc)

def get_min_sort_val(db, list_id):
    collection = db['cards']
    query = {'archived': False, 'listId': list_id}
    projection = {'_id': -1, 'sort':1}
    cursor = collection.find(query, projection).sort('sort', 1).limit(1)
    docs = list(cursor)
    return docs[0]['sort']

def get_today_str():
    today = datetime.today()
    return datetime.strftime(today, '%d.%m')

if __name__ == '__main__':
    main()