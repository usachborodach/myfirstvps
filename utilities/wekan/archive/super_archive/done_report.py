from pymongo import MongoClient
import path_depended.utilities.wekan.get_id as get_id
from datetime import datetime, time, timedelta

client = MongoClient('mongodb://172.29.1.9:27017/')
db = client['wekan']
cards = db['cards']

chosen_day = (datetime.now() - timedelta(days=1)).date()
min_datetime = datetime.combine(chosen_day, time.min)
max_datetime = datetime.combine(chosen_day, time.max)

board_title = 'work'
board_id = get_id.by_title('boards', board_title)
query = {"boardId": board_id, "archivedAt": {"$gte": min_datetime, "$lte": max_datetime}}
projection = {"title": 1, "_id": 0}
documents = list(cards.find(query, projection))

for document in documents:
    print(document['title'])
print(f"\nIn '{board_title}' doned: {len(documents)}")
