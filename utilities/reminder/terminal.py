import os
import logger
from command_handler import command_handler
from datetime import datetime
import csv
import subprocess

subprocess.run(['export', 'TERM=xterm'])

interface_height = 19
interface_width = 80

def print_interface():
    try:
        reminders = csv.load()
        os.system("clear")
        print("id | date  | per | brd  | a | text                                            ")
        reminder_status = 0
        print_separator("expired:")
        for index, reminder in enumerate(reminders):
            if index == interface_height:
                break
            reminder_datetime = datetime.strptime(reminder["date"], "%Y.%m.%d")
            if reminder_datetime == logger.current_date and reminder_status == 0:
                reminder_status = 1
                print_separator("today:")
            if reminder_datetime > logger.current_date and reminder_status < 2:
                reminder_status = 2
                print_separator("planned:")
            print_line(index, reminder)
        logger.log_debug("Interface printed successfully")
    except Exception as e:
        logger.log_error(f"Error printing interface: {str(e)}")

def print_separator(text):
    separator = text + "=" * (interface_width - len(text))
    print(separator)

def print_line(index, reminder):
    line = (
        f"{print_cell(index, 2)}"
        f"{print_cell(reminder['date'][5:], 5)}"
        f"{print_cell(reminder['period'], 3)}"
        f"{print_cell(reminder['board'], 4)}"
        f"{print_cell(reminder['auto'], 1)}"
        f"{print_cell(reminder['text'], 47)}" )
    print(line)

def print_cell(text, cell_size):
    text = str(text)
    if len(text) < cell_size:
        return text.ljust(cell_size) + " | "
    return text[:cell_size] + " | "

os.chdir(os.path.dirname(__file__))
logger.log_debug("Application started in interactive mode")
while True:
    print_interface()
    command_handler()