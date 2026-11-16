import logger
import csv

def delete(index):
    reminders = csv.load()
    try:
        rem_text = reminders[index]['text']
        del reminders[index]
        csv.dump(reminders)
        logger.log_info(f"Deleted reminder '{rem_text}'")
    except Exception as e:
        logger.log_error(f"Error deleting reminder '{reminders[index]['text']}': {str(e)}")