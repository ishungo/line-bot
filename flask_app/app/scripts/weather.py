from datetime import datetime as dt
from dotenv import load_dotenv
from pathlib import Path
import os
import pytz
import requests
jst = pytz.timezone('Asia/Tokyo')
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = SCRIPT_DIR.parent.parent.parent / '.env'
load_dotenv(str(ENV_DIR))
WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]



def make_weather_prompt():
    now = dt.now(jst)
    year = now.year
    month = now.month
    day = now.day
    weekday = WEEKDAYS[now.weekday()]
    # hour = now.hour
    # minute = now.minute
    # second = now.second
    weather_prompt = "\n上記の文章はどの都市の何月何日の天気について尋ねている文章ですか？"
    weather_prompt += f"\n現在の日時は{year}年{month}月{day}日{weekday}曜日です"
    weather_prompt += "\n以下の形式で都市名と日にちを回答してください."
    weather_prompt += "\n回答例1: TOKYO 7月10日月曜日"
    weather_prompt += "\n回答例2: OSAKA 12月13日火曜日"
    return weather_prompt


def get_weather(city, date):
    if date.date() == dt.now(jst).date():
        ret = get_weather_current(city)
    else:
        ret = get_weather_forecast(city, date)
    return ret

def get_weather_current(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q": city,
        "units": "metric",
        "appid": WEATHER_API_KEY,
    }
    # complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        data = response.json()

        main_dat = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        sys = data["sys"]

        temp = main_dat["temp"]
        temp_min = main_dat["temp_min"]
        temp_max = main_dat["temp_max"]
        pressure = main_dat["pressure"]
        humidity = main_dat["humidity"]
        description = weather["description"]
        wind_speed = wind["speed"]
        wind_deg = wind["deg"]
        sunrise = sys["sunrise"]
        sunset = sys["sunset"]

        ret = f"{sys['country']}にある{data['name']}の現在の天気は以下の通りです"
        ret += f"\n天気: {description.capitalize()}"
        ret += f"\n気温: {temp}°C"
        ret += f"\n最低気温: {temp_min}°C"
        ret += f"\n最高気温: {temp_max}°C"
        ret += f"\n気圧: {pressure} hPa"
        ret += f"\n湿度: {humidity}%"
        ret += f"\n風速: {wind_speed} m/s"
        ret += f"\n風向: {wind_deg}°"
        ret += f"\n日の出: {to_jst(dt.fromtimestamp(sunrise))}"
        ret += f"\n日没: {to_jst(dt.fromtimestamp(sunset))}"
    elif response.status_code == 404:
        ret = "天気の取得に失敗しました"
    else:
        ret = "エラーが発生しました"
    return ret


def get_weather_forecast(city, date):
    print(f"{city}の{date}の天気を問い合わせます")
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    # pprint(data)
    ret = ""
    if response.status_code == 200:
        city = data["city"]['name']
        country = data["city"]['country']

        for i in range(len(data["list"])):
            dt_txt = data["list"][i]["dt_txt"]
            dt_obj = dt.fromisoformat(dt_txt)
            if dt_obj.date() != date.date(): continue
            if dt_obj.hour != 12: continue

            weather = data["list"][i]["weather"][0]
            wind = data["list"][i]["wind"]
            main_dat = data["list"][i]["main"]
            temp = main_dat["temp"]
            temp_min = main_dat["temp_min"]
            temp_max = main_dat["temp_max"]
            pressure = main_dat["pressure"]
            humidity = main_dat["humidity"]
            description = weather["description"]
            wind_speed = wind["speed"]
            wind_deg = wind["deg"]
            ret  = f"{country}にある{city}の天気は以下の通りです"
            ret += f"\n日時: {to_jst(dt.fromisoformat(dt_txt))}"
            ret += f"\n天気: {description.capitalize()}"
            ret += f"\n気温: {temp}°C"
            ret += f"\n最低気温: {temp_min}°C"
            ret += f"\n最高気温: {temp_max}°C"
            ret += f"\n気圧: {pressure} hPa"
            ret += f"\n湿度: {humidity}%"
            ret += f"\n風速: {wind_speed} m/s"
            ret += f"\n風向: {wind_deg}°"
            ret += "\n\n"
    elif response.status_code == 404 or ret == "":
        ret = f"{city}の{date.strftime('%m月%d日')}の天気は取得できませんでした"
    else:
        ret = "エラーが発生しました"
    return ret


def to_jst(dt):
    return dt.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S')


def main():
    pass

if __name__ == '__main__':
    main()
