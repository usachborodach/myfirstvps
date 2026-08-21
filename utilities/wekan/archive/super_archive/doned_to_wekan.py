import os, requests, json
base_path = os.path.dirname(__file__)
WEKAN_ADDRESS = '172.29.1.9:2000'
ids_path = os.path.join(base_path, 'ids.json')
ids = json.loads(open(ids_path, encoding='utf-8').read())
BOARD_ID = ids['board_id']
successfull_counter = 0

def get_token():
    auth_url = f'http://{WEKAN_ADDRESS}/users/login'
    auth_data = {'username': 'agorbov', 'password': 'Sven159357258'}
    token = json.loads(requests.post(auth_url, data=auth_data).text)['token']
    return token

def post_the_card(text_input, list_name, swimlane_name, token):
    global successfull_counter
    post_the_card_url = f"http://{WEKAN_ADDRESS}/api/boards/{BOARD_ID}/lists/{ids['lists'][list_name]}/cards"
    headers = {'Authorization': f'Bearer {token}'}
    request_data = {
        'title': f'{text_input}',
        'description': '',
        'authorId': ids['author_id'],
        'swimlaneId': f"{ids['swimlanes'][swimlane_name]}"
    }
    try:
        requests.post(post_the_card_url, headers=headers, data=request_data).text
    except Exception as exception_text:
        print(exception_text)
        input()
    else:
        successfull_counter += 1

token = get_token()
csv_path = os.path.join(base_path, 'doned.csv')
csv = open(csv_path, encoding='utf-8').read().splitlines()
res = dict()
for line in csv:
    line= line.split(';')
    if line[1] == str() and line[2] == str():
        last_key = line[0]
        res[last_key] = {"Работа. Надо": list(), "Личные": list()}
    else:
        if line[1] != str():
            res[last_key]["Работа. Надо"].append(line[1])
        if line[2] != str():
            res[last_key]["Работа. Надо"].append(line[2])
            
out_path = os.path.join(base_path, 'out.json')
with open(out_path, 'w', encoding='utf-8') as fp:
    json.dump(res, fp, ensure_ascii=False, indent=4)

for swimlane, lists in res.items():
    print(swimlane)
    for list_name, cards in lists.items():
        print(list_name)
        for card in cards:
            print(card)
            post_the_card(card, list_name, swimlane, token)
    
print(f'successfull_moved_tasks: {successfull_counter}')