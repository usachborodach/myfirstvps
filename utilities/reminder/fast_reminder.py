import sys
import time
import os
import telebot
from datetime import datetime
from dotenv import load_dotenv

def daemonize():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print(f"Ошибка при создании дочернего процесса: {e}")
        sys.exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)

print('fast_reminder')
text = input('text: ')
delay = input('delay: ')

if delay.endswith('h'):
    delay = int(delay[:-1]) * 60
elif ':' in delay:
    today = datetime.strftime(datetime.now(), '%y.%m.%dT')
    chosen_time = datetime.strptime(today + delay, '%y.%m.%dT%H:%M')
    delay = chosen_time - datetime.now()
    delay = str(delay).split(':')
    hours, minutes = int(delay[0]), int(delay[1])
    delay = hours * 60 + minutes
elif delay.isdigit():
    delay = int(delay)

daemonize()
time.sleep(delay * 60)
load_dotenv()
bot = telebot.TeleBot(os.getenv('MESSAGE_SENDER'))
bot.send_message(-994724508, text)