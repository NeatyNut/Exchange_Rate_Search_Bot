from discord import send_message
from JPYKRW import get_currency
from googlesheet import insert_row
import time

while True:
    date, times, price, updown, percent = get_currency()
    insert_row(date, times, price, updown, percent)
    send_message(f"{date} {times} 기준, 엔화 가격은 {price}원으로 전일 대비 {updown}, {percent}")
    time.sleep(1800)
