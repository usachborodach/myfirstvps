from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import csv
import logger

def postpone(index):
    reminders = csv.load()
    try:
        period = reminders[index]['period']
        period_num = int(period[:-1])
        period_unit = period[-1]
        date_increment = (
            timedelta(days=period_num) if period_unit == 'd' else
            relativedelta(months=period_num) if period_unit == 'm' else
            relativedelta(years=period_num))
        postpone_date = logger.current_date + date_increment
        reminders[index]["date"] = postpone_date.strftime("%Y.%m.%d")
        reminders[index]["sended"] = '0'
        csv.dump(reminders)
        logger.log_info(f"Postponed reminder '{reminders[index]['text']}' to {reminders[index]['date']}")
    except Exception as e:
        logger.log_error(f"Error while postpone '{reminders[index]['text']}': {str(e)}")