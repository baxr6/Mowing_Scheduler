
from datetime import timedelta

def get_nth_working_day(start_date, n, skipped_dates):
    current = start_date
    count = 0
    while count < n:
        current += timedelta(days=1)
        if current not in skipped_dates:
            count += 1
    return current
