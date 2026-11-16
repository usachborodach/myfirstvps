from datetime import datetime, timedelta
def print_spreadsheet():
    top =    '┌' + ((('─' * 28) +       '┬') * 6) + ('─' * 28) + '┐' + '\n'
    cell = (('│' + (  ' ' * 28)) * 7) + '│' + '\n'
    middle = '├' + ((('─' * 28) +       '┼') * 6) + ('─' * 28) + '┤' + '\n'
    bottom = '└' + ((('─' * 28) +       '┴') * 6) + ('─' * 28) + '┘'
    screen = top + (((cell * 10) + middle) * 4) + (cell * 8) + bottom
    print(screen)

def make_current_week():
    chosen_day = datetime.today()
    current_week = [chosen_day]
    while chosen_day.weekday() > 0:
        chosen_day -= timedelta(days=1)
        current_week.insert(0, chosen_day)
    chosen_day = datetime.today()
    while len(current_week) < 7:
        chosen_day += timedelta(days=1)
        current_week.append(chosen_day)
    return current_week

def make_current_month():
    month = [make_current_week()]
    last_day = month[0][-1]
    for new_week in range(4):
        new_week = list()
        for day in range(7):
            last_day += timedelta(days=1)
            new_week.append(last_day)
        month.append(new_week)
    return month