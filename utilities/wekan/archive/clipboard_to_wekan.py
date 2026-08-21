import pyperclip
from path_depended.utilities.wekan.post_card import post_card
import socket

def workpc_parse(loc_input_text):
    loc_input_text = loc_input_text.split(']\n')
    del loc_input_text[0]
    res = list()
    for i in loc_input_text:
        res.append(i.rsplit('\n', 2)[0])
    return res

def otherpc_parse(loc_input_text):
    loc_input_text = loc_input_text.split('] Aleksandr Gorbov: ')
    del loc_input_text[0]
    res = list()
    for i in loc_input_text:
        res.append(i.rsplit('\n', 1)[0])
    return res

if __name__ == '__main__':
    input_text = pyperclip.paste()
    hostname =  socket.gethostname()
    if hostname == "work-pc":
        messages = workpc_parse(input_text)
    else:
        messages = otherpc_parse(input_text)
    for message in messages:
        post_card(message, 'work')
        print(f'"{message}"')
    print(f'\n{len(messages)} tasks successfull posted to "work" board')