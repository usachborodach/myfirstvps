from os import system
from time import sleep
from pyperclip import paste
from post_card import post_card

print('Вырежи текст из заметки, вернись сюда и нажми enter')
sleep(2)
system('xdg-open "https://keep.google.com/#NOTE/18qUqzvWv8ako0Nb17EwvO_I_-dAE8mcuE-K0pCl1fxgDqGvB7asGpdASPYUp-Dszg9_hgw"')
input()
text = paste()

if text == "пусто" or text == "empty":
    print('There is no tasks. Skipped')
    exit()

text = text.split('\n\n')
for i in text:
    print(f'"{i}"')
    post_card(i, 'work')
print(f'\n{len(text)} tasks successfull posted to "work" board')