import common
from datetime import datetime
import is_working_day

def main():
    if is_working_day.main():
        today_str = get_today_str()
        token = common.get_token()
        card_id = common.post_card(today_str, 'work', 'Дейлик', token)
        client, db = common.connect_to_mongo()
        min_sort_val = get_min_sort_val(db)
        set_sort_val(db, card_id, min_sort_val)
        client.close()

def set_sort_val(db, card_id, min_sort_val):
    collection = db['cards']
    query = {'_id': card_id}
    decremented_sort_val = min_sort_val - 1
    operation = {'$set': {'sort': decremented_sort_val}}
    collection.update_one(query, operation)

def get_min_sort_val(db):
    collection = db['cards']
    list_id = common.get_list_id('work', 'Дейлик')
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