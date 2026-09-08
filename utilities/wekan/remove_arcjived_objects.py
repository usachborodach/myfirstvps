from common import connect_to_mongo

client, db = connect_to_mongo()
col_names = ['cards', 'lists']
for col_name in col_names:
    collection = db[col_name]
    query = {'archived': True}
    count = collection.count_documents(query)
    print(count)
