import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from datetime import datetime

class bot:
    def __init__(self, start=0):
        load_dotenv()
        self.headers = {
        'User-Agent': 'Mozilla/5.0'
        }
        self.start = start
        self.INDEX_URL = os.getenv("INDEX_URL")
        self.CURRUNCY = os.getenv("CURRUNCY")
        self.JAP = os.getenv("JAP")
        self.USA = os.getenv("USA")
        self.EU = os.getenv("EU")
        self.CN = os.getenv("CN")
        self.OILGOLD = os.getenv("OILGOLD")
        self.WOIL = os.getenv("WOIL")
        self.KOIL = os.getenv("KOIL")
        self.WGOLD = os.getenv("WGOLD")
        self.KGOLD = os.getenv("KGOLD")
        self.NUM = os.getenv("NUM")
        self.CHANGE = os.getenv("CHANGE")
        self.UPDOWN = os.getenv("UPDOWN")
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        self.max_trial = 5
        self.order = {self.CURRUNCY:[self.USA, self.JAP, self.EU, self.CN], self.OILGOLD:[self.WOIL, self.KOIL, self.WGOLD, self.KGOLD]}
        self.order2 = [self.NUM, self.CHANGE, self.UPDOWN]
        self.indexs = {
            self.USA:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.JAP:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.EU:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.CN:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.WOIL:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.KOIL:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.WGOLD:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False},
            self.KGOLD:{self.NUM:0, self.CHANGE:"", "high":0, "low":0,"show":False}}

    def scrap(self):
        response = requests.get(self.INDEX_URL, headers=self.headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            for k, vals in self.order.items():
                for idx, val in enumerate(vals):
                    for what in self.order2:
                        value = soup.select_one(f"#{k} > li.on > a.head.{val} > div > span.{what}")
                        if not value:
                            value = soup.select_one(f"#{k} > li:nth-child({idx+1}) > a.head.{val} > div > span.{what}")

                        value = value.get_text().replace(",","")

                        if what == self.UPDOWN: ## UPDOWN이라면
                            if value == "상승":
                                self.indexs[val][self.CHANGE] = "▲ " + self.indexs[val][self.CHANGE]
                            else :
                                self.indexs[val][self.CHANGE] = "▼ " + self.indexs[val][self.CHANGE]

                        elif what == self.NUM:  ## value라면
                            ex_value = self.indexs[val][self.NUM]

                            if ex_value != 0:
                                numbers = [ex_value, float(value)]
                                change_rate = (max(numbers) - min(numbers))

                                if change_rate >= 0.02:
                                    self.indexs[val]["show"] = True

                                self.indexs[val]["high"] = float(value)
                                self.indexs[val]["low"] = float(value)
                            else :
                                self.indexs[val]["high"] = max(float(value), self.indexs[val]["high"])
                                self.indexs[val]["low"] = min(float(value), self.indexs[val]["low"])

                            self.indexs[val][self.NUM] = float(value)
                        
                        elif what == self.CHANGE:
                            self.indexs[val][self.CHANGE] = value

    def report(self, option=None):
        message = ""
        now = datetime.now()
        
        if option:
            if option == "start":
                message = f"""
                <{now.strftime("%H:%M")}>
                
                <환율>
                미국 달러 환율 : {self.indexs[self.USA][self.NUM]:,.2f}원(전일 대비 {self.indexs[self.USA][self.CHANGE]})
                일본 엔화 환율 : {self.indexs[self.JAP][self.NUM]:,.2f}원(전일 대비 {self.indexs[self.JAP][self.CHANGE]})
                유럽 유로 환율 : {self.indexs[self.EU][self.NUM]:,.2f}원(전일 대비 {self.indexs[self.EU][self.CHANGE]})
                중국 위안화 환율 : {self.indexs[self.CN][self.NUM]:,.2f}원(전일 대비 {self.indexs[self.CN][self.CHANGE]})
                
                <유가>
                국제 유가 : {self.indexs[self.WOIL][self.NUM]:,.2f}달러(전일 대비 {self.indexs[self.WOIL][self.CHANGE]})
                국내 유가 : {self.indexs[self.KOIL][self.NUM]:,.2f}원(전일 대비 {self.indexs[self.KOIL][self.CHANGE]})
                
                <금 시세>
                국제 금 시세 : {self.indexs[self.WGOLD][self.NUM]:,.2f}달러(전일 대비 {self.indexs[self.WGOLD][self.CHANGE]})
                국내 금 시세 : {self.indexs[self.KGOLD][self.NUM]:,.2f}원(전일 대비 {self.indexs[self.KGOLD][self.CHANGE]})
                """

            elif option == "end":
                message = f"""
                <{now.strftime("%H:%M")}>

                <환율>
                미국 달러 환율 : {self.indexs[self.USA][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.USA][self.CHANGE]}, 금일 최고가 : {self.indexs[self.USA]["high"]}원, 금일 최저가 : {self.indexs[self.USA]["low"]}원)
                일본 엔화 환율 : {self.indexs[self.JAP][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.JAP][self.CHANGE]}, 금일 최고가 : {self.indexs[self.JAP]["high"]}원, 금일 최저가 : {self.indexs[self.JAP]["low"]}원)
                유럽 유로 환율 : {self.indexs[self.EU][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.EU][self.CHANGE]}, 금일 최고가 : {self.indexs[self.EU]["high"]}원, 금일 최저가 : {self.indexs[self.EU]["low"]}원)
                중국 위안화 환율 : {self.indexs[self.CN][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.CN][self.CHANGE]}, 금일 최고가 : {self.indexs[self.CN]["high"]}원, 금일 최저가 : {self.indexs[self.CN]["low"]}원)
                
                <유가>
                국제 유가 : {self.indexs[self.WOIL][self.NUM]:,.2f}달러 (전일 대비 {self.indexs[self.WOIL][self.CHANGE]}, 금일 최고가 : {self.indexs[self.WOIL]["high"]}달러, 금일 최저가 : {self.indexs[self.WOIL]["low"]}달러)
                국내 유가 : {self.indexs[self.KOIL][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.KOIL][self.CHANGE]}, 금일 최고가 : {self.indexs[self.KOIL]["high"]}원, 금일 최저가 : {self.indexs[self.KOIL]["low"]}원)

                <금 시세>
                국제 금 시세 : {self.indexs[self.WGOLD][self.NUM]:,.2f}달러 (전일 대비 {self.indexs[self.WGOLD][self.CHANGE]}, 금일 최고가 : {self.indexs[self.WGOLD]["high"]}달러, 금일 최저가 : {self.indexs[self.WGOLD]["low"]}달러)
                국내 금 시세 : {self.indexs[self.KGOLD][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.KGOLD][self.CHANGE]}, 금일 최고가 : {self.indexs[self.KGOLD]["high"]}원, 금일 최저가 : {self.indexs[self.KGOLD]["low"]}원)
                """
            
        else :
            message += f"미국 달러 환율 : {self.indexs[self.USA][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.USA][self.CHANGE]}, 금일 최고가 : {self.indexs[self.USA]["high"]}원, 금일 최저가 : {self.indexs[self.USA]["low"]}원)\n" if self.indexs[self.USA]["show"] else ""
            message += f"일본 엔화 환율 : {self.indexs[self.JAP][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.JAP][self.CHANGE]}, 금일 최고가 : {self.indexs[self.JAP]["high"]}원, 금일 최저가 : {self.indexs[self.JAP]["low"]}원)\n" if self.indexs[self.JAP]["show"] else ""
            message += f"유럽 유로 환율 : {self.indexs[self.EU][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.EU][self.CHANGE]}, 금일 최고가 : {self.indexs[self.EU]["high"]}원, 금일 최저가 : {self.indexs[self.EU]["low"]}원)\n" if self.indexs[self.EU]["show"] else ""
            message += f"중국 위안화 환율 : {self.indexs[self.CN][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.CN][self.CHANGE]}, 금일 최고가 : {self.indexs[self.CN]["high"]}원, 금일 최저가 : {self.indexs[self.CN]["low"]}원)\n" if self.indexs[self.CN]["show"] else ""
            message += f"국제 유가 : {self.indexs[self.WOIL][self.NUM]:,.2f}달러 (전일 대비 {self.indexs[self.WOIL][self.CHANGE]}, 금일 최고가 : {self.indexs[self.WOIL]["high"]}달러, 금일 최저가 : {self.indexs[self.WOIL]["low"]}달러)\n" if self.indexs[self.WOIL]["show"] else ""
            message += f"국내 유가 : {self.indexs[self.KOIL][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.KOIL][self.CHANGE]}, 금일 최고가 : {self.indexs[self.KOIL]["high"]}원, 금일 최저가 : {self.indexs[self.KOIL]["low"]}원)\n" if self.indexs[self.KOIL]["show"] else ""
            message += f"국제 금 시세 : {self.indexs[self.WGOLD][self.NUM]:,.2f}달러 (전일 대비 {self.indexs[self.WGOLD][self.CHANGE]}, 금일 최고가 : {self.indexs[self.WGOLD]["high"]}달러, 금일 최저가 : {self.indexs[self.WGOLD]["low"]}달러)\n" if self.indexs[self.WGOLD]["show"] else ""
            message += f"국내 금 시세 : {self.indexs[self.KGOLD][self.NUM]:,.2f}원 (전일 대비 {self.indexs[self.KGOLD][self.CHANGE]}, 금일 최고가 : {self.indexs[self.KGOLD]["high"]}원, 금일 최저가 : {self.indexs[self.KGOLD]["low"]}원)" if self.indexs[self.KGOLD]["show"] else ""

            if message != "":
                message = f"<{now.strftime("%H:%M")}>\n\n<급변동 이슈>\n" + message

                self.indexs[self.USA]["show"] = False
                self.indexs[self.JAP]["show"] = False
                self.indexs[self.EU]["show"] = False
                self.indexs[self.CN]["show"] = False
                self.indexs[self.WOIL]["show"] = False
                self.indexs[self.KOIL]["show"] = False
                self.indexs[self.WGOLD]["show"] = False
                self.indexs[self.KGOLD]["show"] = False
        
        message = message.replace("  ", "")
        
        return message
    
    def send_message(self, message:str, trial=1):
        data = {
            "content": message
        }

        response = requests.post(self.WEBHOOK_URL, json=data)

        if not response.status_code == 204 and trial <= self.max_trial:
            self.send_message(message, trial+1)

    def run(self):
        
        for i in range(self.start, 34):
            try :
                self.scrap()
                if i == 0:
                    message = self.report(option="start")
                elif i == 33:
                    message = self.report(option="end")
                else :
                    message = self.report()
                
                self.send_message(message)
            except Exception as e :
                try :
                    self.send_message(f"Unknow error : {e}")
                    return False
                except :
                    return False
            
            time.sleep(1800)
            
        return True