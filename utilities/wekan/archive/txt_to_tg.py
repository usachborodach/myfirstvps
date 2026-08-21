txt = '''test
test
test'''

fridge = -4185749031
outside = -894095483
chosen_chat = outside

import  telebot, time
bot = telebot.TeleBot('5641565819:AAFS-GmkHOHXeK12TClRCZB_Gh8ZKRHBRQs')
for index, line in enumerate(txt.splitlines()):
    while True:
        try:
            bot.send_message(chosen_chat, line)
        except telebot.apihelper.ApiTelegramException as excepton_text:
            delay = int(str(excepton_text).split()[-1])
            for i in range(delay):
                print(f'Wait {delay - i} from {delay}')
                time.sleep(1)
        else:
            print(f'{index + 1}. {line}')
            break
print('done')