from pymongo import MongoClient
import get_id

client = MongoClient('mongodb://172.29.1.9:27017/')
db = client['wekan']
cards = db['cards']

board_title = 'work'
list_title = 'Новые'

list_id = get_id.by_title_and_board('lists', list_title, board_title)
query = { "listId": list_id, "archived": False }

result = cards.delete_many(query)
print(f"Удалено документов: {result.deleted_count}")