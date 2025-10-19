# from JPYKRW import get_currency
# from googlesheet import insert_row
import time
from bot import bot
from datetime import datetime, time
import scheduler

if __name__ == "__main__":
    while True:
        # date, times, price, updown, percent = get_currency()
        # insert_row(date, times, price, updown, percent)
        # send_message(f"{date} {times} 기준, 대만TWD 가격은 {price}원으로 전일 대비 {updown}, {percent}")
        
        now = datetime.now().time()
        if time(2, 0) < now < time(9, 0):
            sleep_seconds = scheduler.waiting()
            time.sleep(sleep_seconds)
            continue
        else :
            reply = scheduler.check_reply()

        search_bot = bot(reply=reply)
        if search_bot.run():
            sleep_seconds = scheduler.waiting()
            del search_bot
            time.sleep(sleep_seconds)
        else :
            break
