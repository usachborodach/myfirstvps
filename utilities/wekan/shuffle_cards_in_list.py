import argparse
from random import shuffle
import common

"""
python3 \
/home/user/repos/ShuraRepo/path_depended/utilities/wekan/shuffle_cards_in_list.py \
--board_title="work" \
--list_title="Завтра"
"""

def shuffle_cards_in_list(board_title, list_title):
    client, db = common.connect_to_mongo()
    collection = db['cards']
    list_id = common.get_list_id(db, board_title, list_title)
    query = {"listId": list_id, "archived": False}
    projection = {'_id': 1}
    cursor = collection.find(query, projection)
    documents = list(cursor)
    shuffle(documents)
    for index, document in enumerate(documents):
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"sort": index}})
    client.close()

def process_the_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_title')
    parser.add_argument('--list_title')
    args = parser.parse_args()
    return args.board_title, args.list_title

if __name__ == "__main__":
    board_title, list_title = process_the_arguments()
    shuffle_cards_in_list(board_title, list_title)