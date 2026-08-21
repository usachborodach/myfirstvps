import csv
import subprocess
import yaml
import common

csv_filename = 'cards_export.csv'
temp_dir = '/home/user/Downloads/'

# алиас
# открытие карточки в браузере по айди

def main():
    board_title, list_title = nano_dialogue()
    client, db = common.connect_to_mongo()
    cards = get_cards(db, board_title, list_title)
    save_to_csv(cards, csv_filename)
    open_in_vscode(csv_filename)
    client.close()

def nano_dialogue():
    yml_template = {'board_title': 'work', 'list_title': 'Покодить'}
    yml_name = 'temp.yml'
    yml_path = temp_dir + yml_name
    with open(yml_path, 'w') as fp:
        yaml.safe_dump(yml_template, fp, allow_unicode=True)
    subprocess.run(['nano', yml_path])
    yml_file = open(yml_path)
    data = yaml.safe_load(yml_file)
    return data['board_title'], data['list_title']

def open_in_vscode(csv_filename):
    path = temp_dir + csv_filename
    subprocess.run(['code', path])

def get_cards(db, board_title, list_title):
    list_id = common.get_list_id(db, board_title, list_title)
    collection = db['cards']
    query = {'listId': list_id, 'archived': False}
    projection = {'title': 1, 'createdAt': 1, 'modifiedAt': 1, 'sort': 1}
    cursor = collection.find(query, projection).sort({'sort': 1})
    documents = list(cursor)
    return documents

def save_to_csv(documents, csv_filename):
    path = temp_dir + csv_filename
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=documents[0].keys(), extrasaction='ignore')
        writer.writeheader()
        for doc in documents:
            row = doc.copy()
            for key in ['createdAt', 'modifiedAt', 'dateLastActivity']:
                if key in row and row[key] is not None:
                    row[key] = row[key].isoformat()
                    row[key] = row[key].split('T')[0].replace('-', '.')
            writer.writerow(row)

if __name__ == '__main__':
    main()