from dotenv import load_dotenv
import os
import requests

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_message(message:str):
    data = {
        "content": message
    }

    response = requests.post(WEBHOOK_URL, json=data)

    if not response.status_code == 204:
        send_message(message)