from datetime import datetime
import csv
import logger
from send_to_tg_and_wekan import send_to_tg_and_wekan
from postpone import postpone

def check_reminders():
    reminders = csv.load()
    for index, reminder in enumerate(reminders):
        if datetime.strptime(reminder["date"], "%Y.%m.%d") <= logger.current_date and reminder['sended'] == '0':
            send_to_tg_and_wekan(index)
            if reminder['auto'] == '1':
                postpone(index)
                logger.log_info(f"Auto-postponed reminder '{reminders[index]['text']}'")
                return False
    return True

try:
    logger.log_debug("Running auto reminders check")
    all_reminders_checked = False
    while not all_reminders_checked:
        all_reminders_checked = check_reminders()
    logger.log_info("Auto reminders check completed")

except Exception as e:
    logger.log_error(f"Error in auto function: {str(e)}")