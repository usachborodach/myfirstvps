import os
import yaml
from myfirstvps.utilities.api_client.crud import get_all_docs

base_path = os.path.dirname(__file__)
os.chdir(base_path)

dbs = {
    'quote_gun': 'quotes',
    'tracker': 'days'
}

for db, collection in dbs.items():
    docs = get_all_docs(db, collection)
    with open(f'{db}.{collection}.yml', 'w') as fp:
        yaml.safe_dump(docs, fp, allow_unicode=True)