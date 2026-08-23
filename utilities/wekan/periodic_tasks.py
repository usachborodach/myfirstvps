from datetime import datetime
from move_cards_between_lists import move_cards_between_lists
from shuffle_cards_in_list import shuffle_cards_in_list
from create_sep_in_daily import main as create_sep_in_daily

def main():
    day, day_of_week = get_days()
    if day_of_week == 'Saturday' and day <= 7:
        monthly()
    if day_of_week == 'Sunday':
        weekly()
    daily()

def get_days():
    now = datetime.now()
    day = now.day
    day_of_week = now.strftime("%A")
    return day, day_of_week

def daily():
    move_cards_between_lists('work', 'Завтра', 'Новые')
    move_cards_between_lists('home', 'Завтра', 'Новые')
    shuffle_cards_in_list('work', 'Новые')
    shuffle_cards_in_list('home', 'Новые')
    create_sep_in_daily()

def weekly():
    move_cards_between_lists('work', 'На следующей неделе', 'Новые')
    move_cards_between_lists('home', 'На следующей неделе', 'Новые')

def monthly():
    move_cards_between_lists('work', 'В следующем месяце', 'Новые')
    move_cards_between_lists('home', 'В следующем месяце', 'Новые')

if __name__ == '__main__':
    main()