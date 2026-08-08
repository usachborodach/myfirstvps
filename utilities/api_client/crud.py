import os
import requests
import json
import sys

base_path = os.path.dirname(__file__)
sys.path.append(f'{base_path}/../../')
from utilities.api_server.app.config import settings

def main():
    docs = get_all_docs('quote_gun', 'quotes')
    for doc in docs:
        del doc['_id']
    import yaml
    with open('/tmp/quote_gun.yml', 'w') as fp:
        yaml.safe_dump(docs, fp, allow_unicode=True)

def get_all_docs(db, collection):
    url = f"{settings.BASE_API_URL}/mongo/{db}/{collection}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return data

def create_document(db, collection, document):
    url = f"{settings.BASE_API_URL}/mongo/{db}/{collection}"
    response = requests.post(url, headers=get_headers(), json=document)
    response.raise_for_status()
    print(response.json())
    return response.json()

def delete_document(db, collection, doc_id):
    url = f"{settings.BASE_API_URL}/mongo/{db}/{collection}/{doc_id}"
    response = requests.delete(url, headers=get_headers())
    response.raise_for_status()
    print(response.json())
    return response.json()

def update_document(db, collection, doc_id, new_data):
    url = f"{settings.BASE_API_URL}/mongo/{db}/{collection}/{doc_id}"
    response = requests.put(url, headers=get_headers(), json=new_data)
    response.raise_for_status()
    print(response.json())
    return response.json()

def get_headers():
    return {
        "Authorization": f"Bearer {os.getenv('TOKEN')}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    main()