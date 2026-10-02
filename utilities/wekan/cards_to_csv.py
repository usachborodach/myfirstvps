import csv
import subprocess
import common

# открытие карточки в браузере по айди

CSV_PATH = '/tmp/cards_export.csv'
BOARD_TITLE = 'work'
LIST_TITLES = ['Новые', 'Сегодня', 'Завтра']

def main():
    cards = get_cards()
    save_to_csv(cards)
    open_in_vscode()

def get_cards():
    documents = list()
    client, db = common.connect_to_mongo()
    collection = db['cards']
    for list_title in LIST_TITLES:
        list_id = common.get_list_id(db, BOARD_TITLE, list_title)
        query = {'listId': list_id, 'archived': False}
        projection = {'title': 1, 'createdAt': 1, 'modifiedAt': 1, 'sort': 1}
        cursor = collection.find(query, projection).sort({'sort': 1})
        documents += list(cursor)
    client.close()
    return documents

def save_to_csv(documents):
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=documents[0].keys(), extrasaction='ignore')
        writer.writeheader()
        for doc in documents:
            row = doc.copy()
            for key in ['createdAt', 'modifiedAt', 'dateLastActivity']:
                if key in row and row[key] is not None:
                    row[key] = row[key].isoformat()
                    row[key] = row[key].split('T')[0].replace('-', '.')
            writer.writerow(row)

def open_in_vscode():
    subprocess.run(['code', CSV_PATH])

if __name__ == '__main__':
    main()