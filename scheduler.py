from datetime import datetime, timedelta

def waiting():
    now = datetime.now() 
    next_run = now + timedelta(days=1)
    next_run = next_run.replace(hour=9, minute=1)
    sleep_seconds = (next_run - now).total_seconds()
    return sleep_seconds

def check_reply():
    now = datetime.now()
    start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    elapsed_minutes = (now - start_time).total_seconds() / 60
    elapsed_intervals = int(elapsed_minutes // 30)
    remaining = 34 - elapsed_intervals
    return remaining