# from JPYKRW import get_currency
# from googlesheet import insert_row
from bot import bot
import datetime
import scheduler
import time

if __name__ == "__main__":
    while True:
        # date, times, price, updown, percent = get_currency()
        # insert_row(date, times, price, updown, percent)
        # send_message(f"{date} {times} 기준, 대만TWD 가격은 {price}원으로 전일 대비 {updown}, {percent}")
        
        now = datetime.datetime.now().time()
        if datetime.time(2, 0) < now < datetime.time(9, 0):
            sleep_seconds = scheduler.waiting()
            time.sleep(sleep_seconds)
            continue
        else :
            start = scheduler.check_start()
        search_bot = bot(start=start)
        if search_bot.run():
            del search_bot
        else :
            break
