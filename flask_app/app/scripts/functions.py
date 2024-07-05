
from pathlib import Path
from datetime import datetime as dt
from datetime import timedelta
from pprint import pprint
from .text_generate import generate_text
from .weather import make_weather_prompt, get_weather
import pytz
jst = pytz.timezone('Asia/Tokyo')

MODE_PROMPT = "\n上記の文章は、以下のどの選択肢に該当する文章ですか？"
MODE_PROMPT += "\n1. 天気について尋ねる文章"
MODE_PROMPT += "\n2. その他の質問"
MODE_PROMPT += "\n回答は「1」もしくは「2」のように数字で答えてください"

mode_dict = {
    "挨拶": 0,
    "天気": 1,
    "会話": 2,
}


def str2date(date_str):
    date_str = date_str.replace("月", " ", 1).replace("日", " ", 1).replace("曜", " ", 1)
    date_str = date_str.split()
    month = int(date_str[0])
    day = int(date_str[1])
    now = dt.now()
    date = dt(now.year, month, day)
    return date

def create_responce(msg):
    mode =  get_mode(msg)
    if mode == 0:
        ret = welcome_message()
    elif mode == 1:
        weather_prompt = make_weather_prompt()
        city_date = generate_text(msg + weather_prompt)
        try:
            city, date_str = city_date.split()[-2:]
            date = str2date(date_str)
            ret = get_weather(city, date)
        except:
            ret = "頂いたメッセージの中から地名と日付に関する情報を取得できませんでした。"
    elif mode == 2:
        ret = generate_text(msg)
    else:
        ret = "解析に失敗しました"
    return ret


def get_mode(msg):
    mode = -1
    if msg == "こんにちは":
        mode = 0
    elif len(msg.replace('！', '!').split('!!!')) > 2:
        mode_name = msg.replace('！', '!').split('!!!')[1]
        if mode_name == '天気'  : mode = mode_dict[mode_name]
        elif mode_name == '会話': mode = mode_dict[mode_name]
    else:
        mode_responce = generate_text(msg + MODE_PROMPT)
        if "1" in mode_responce  : mode = 1
        elif "2" in mode_responce: mode = 2
    return mode


def welcome_message():
    ret  = "こんにちは！"
    ret += "\n天気について尋ねる場合はメッセージの先頭に「!!!天気!!!」と入力してください"
    ret += "\nその他の会話をしたい場合はメッセージの先頭に「!!!会話!!!」と入力してください"
    return ret

def main():
    msg = "ubuntuとは何ですか？"
    # model = "gpt-3.5-turbo"
    model = "gpt-4o"
    print(generate_text(msg, model))


if __name__ == "__main__":
    # main()
    tomorrow = dt.now(jst).date() + timedelta(days=1)
    get_weather("Tokyo", dt.now())
