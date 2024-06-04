import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("../.env")
USER_ID = os.getenv("USER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
URL = "https://api.line.me/v2/bot/message/push"

def send_messages(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    data = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    # response = requests.post("http://100.64.1.24:8887/samplesite/main/")
    # リクエスト送信
    response = requests.post(URL, headers=headers, data=json.dumps(data))
    print(response.text)


def main():
    message = "こんにちは"
    send_messages(message)

if __name__ == '__main__':
    main()
