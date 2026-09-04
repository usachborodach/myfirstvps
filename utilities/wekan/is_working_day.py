from datetime import datetime
from typing import Optional

USE_DEBUG_DATE = False
DEBUG_DATE_STR = '26.09.2026'
VACATION_PERIOD = '03.09.2026-16.09.2026'

def main() -> bool:
    date_obj = get_current_or_debug_date(USE_DEBUG_DATE, DEBUG_DATE_STR)
    return is_workday(date_obj)

def str_to_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%d.%m.%Y")

def parse_vacation_period(period_str: str) -> tuple[datetime, datetime]:
    start_str, end_str = period_str.split('-')
    return str_to_date(start_str), str_to_date(end_str)

def is_vacation_day(date_obj: datetime, vacation_period: str = VACATION_PERIOD) -> bool:
    start, end = parse_vacation_period(vacation_period)
    return start <= date_obj <= end

def is_weekend(date_obj: datetime) -> bool:
    return date_obj.strftime("%A") in ('Saturday', 'Sunday')

def get_current_or_debug_date(use_debug: bool = USE_DEBUG_DATE,
                              debug_date: Optional[str] = None) -> datetime:
    if use_debug and debug_date:
        return str_to_date(debug_date)
    return datetime.now()

def is_workday(date_obj: datetime) -> bool:
    return not (is_weekend(date_obj) or is_vacation_day(date_obj))

if __name__ == '__main__':
    main()