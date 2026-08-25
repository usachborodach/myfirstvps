import argparse
import common

"""
python3 \
/home/user/repos/ShuraRepo/path_depended/utilities/wekan/move_cards_between_lists.py \
--board "work" \
--source_list "Завтра" \
--target_list "Новые"
"""

def main():
    board, source_list, target_list = process_the_arguments()
    move_cards_between_lists(board, source_list, target_list)

def process_the_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board')
    parser.add_argument('--source_list')
    parser.add_argument('--target_list')
    args = parser.parse_args()
    return args.board, args.source_list, args.target_list

def move_cards_between_lists(board, source_list, target_list):
    client, db = common.connect_to_mongo()
    collection = db['cards']
    source_list_id = common.get_list_id(board, source_list)
    target_list_id = common.get_list_id(board, target_list)
    query = {"listId": source_list_id, "archived": False}
    new_value = { "$set": { "listId": target_list_id } }
    collection.update_many(query, new_value)
    client.close()

if __name__ == '__main__':
    main()