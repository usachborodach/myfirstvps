import webbrowser
from time import sleep
from pyperclip import paste
import common

def main():
    text = prompt_with_keep()
    items = process_text(text)
    token = common.get_token()
    for item in items:
        common.post_card(item, 'work', 'Новые', token)
        print(f'"{item}"')
    print(f'\n{len(items)} tasks successfull posted to "work" board')

def prompt_with_keep():
    print('Вырежи текст из заметки, вернись сюда и нажми enter')
    sleep(1)
    keep_url = 'https://keep.google.com/'
    note_id = '#NOTE/18qUqzvWv8ako0Nb17EwvO_I_-dAE8mcuE-K0pCl1fxgDqGvB7asGpdASPYUp-Dszg9_hgw'
    webbrowser.open(keep_url + note_id)
    input()
    return paste()

def process_text(text):
    if text == "пусто" or text == "empty":
        print('There is no tasks. Skipped')
        exit()
    return text.split('\n\n')

if __name__ == '__main__':
    main()