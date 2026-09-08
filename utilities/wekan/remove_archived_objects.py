from common import connect_to_mongo

def main():
    client, db = connect_to_mongo()
    col_names = ['cards', 'lists']
    for col_name in col_names:
        collection = db[col_name]
        query = {'archived': True}
        collection.delete_many(query)
    client.close()

if __name__ == '__main__':
    main()