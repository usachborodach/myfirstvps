from datetime import timedelta, date
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import logger
import csv
from calendar_view import make_current_month
from random import choice

def input_with_prefill(message: str, prefill: str = ""):
    bindings = KeyBindings()
    @bindings.add('c-a')
    def clear_text(event):
        event.app.current_buffer.text = ""
    return prompt(message, default=prefill, key_bindings=bindings)

def random_days():
    num = choice([5,6,8,9])
    return f'{num}d'

def random_nearby_date():
    random_num = choice([5,6,8,9])
    today = logger.current_date
    nearby_date = today + timedelta(days=random_num)
    return nearby_date.strftime("%Y.%m.%d")

def get_reminder_fields():
    return {
        'text': input_with_prefill("text: ", str()),
        'date': input_with_prefill("date: ", random_nearby_date()),
        'period': input_with_prefill("period: ", random_days()),
        'auto': input_with_prefill("auto: ", '0'),
        'sended': input_with_prefill("sended: ", '0'),
        'board': input_with_prefill("board: ", 'work') }

def print_month_hint():
    month = make_current_month()
    res = '\nпн вт ср чт пт сб вс\n'
    for week in month:
        for day in week:
            if day.date() == date.today():
                res += '▮▮'
            else:
                res += day.strftime("%d")
            res += ' '
        res += '\n'
    print(res)

try:
    print_month_hint()
    reminder = get_reminder_fields()
    reminder['text'] = reminder['text'].replace('\n', '\\n')
    reminders = csv.load()
    reminders.append(reminder)
    csv.dump(reminders)
    logger.log_info(f"Added reminder '{reminder['text']}' for {reminder['date']} with add.py")
except Exception as e:
    logger.log_error(f"Error while adding new reminder: {str(e)}")
