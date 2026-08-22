import os
import logger

os.chdir(os.path.dirname(__file__))
keys = ["date", "board", "period", "auto", "sended", "text"]

def load():
    try:
        with open("reminders.csv", encoding="utf-8") as file:
            csv = file.read().splitlines()
        del csv[0]
        reminders = []
        for line in csv:
            line = line.split(';')
            reminder = dict(zip(keys, line))
            reminders.append(reminder)
        reminders = sorted(reminders, key=lambda x: x["date"])
        logger.log_debug("Successfully loaded reminders from CSV")
        return reminders
    except Exception as e:
        logger.log_error(f"Error loading CSV: {str(e)}")
        return []

def dump(reminders):
    try:
        reminders = sorted(reminders, key=lambda x: x["date"])
        csv_lines = [';'.join(keys)]
        for reminder in reminders:
            csv_line = ';'.join(reminder[key] for key in keys)
            csv_lines.append(csv_line)
        with open('reminders.csv', 'w', encoding="utf-8") as file:
            file.write('\n'.join(csv_lines))
        logger.log_debug("Successfully saved reminders to CSV")
    except Exception as e:
        logger.log_error(f"Error saving to CSV: {e}")