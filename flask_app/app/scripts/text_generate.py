import os
from pathlib import Path
from datetime import datetime as dt
from dotenv import load_dotenv
from openai import OpenAI
import pytz
jst = pytz.timezone('Asia/Tokyo')


SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = SCRIPT_DIR.parent.parent.parent / '.env'
load_dotenv(str(ENV_DIR))
API_KEY = os.getenv("OPENAI_API_KEY")

GPT_LOG_PATH = SCRIPT_DIR / "gpt_logs" / "gpt_log.txt"
GPT_LOG_PATH.parent.mkdir(exist_ok=True)
GPT_MODEL = os.getenv("GPT_MODEL")

def generate_text(msg):
    client = OpenAI(api_key = API_KEY)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages = [{"role": "user",
                     "content": msg}],
        max_tokens=500,
        temperature=0.1
    )
    ret = response.choices[0].message.content
    time = dt.now(jst).strftime("%Y-%m-%d %H:%M:%S")
    with open(GPT_LOG_PATH, "a", encoding = 'utf-8') as f:
        f.write(f"[Time: {time}]\n")
        f.write(f"Model: {GPT_MODEL}\n")
        f.write(f"Input:\n{msg}\n")
        f.write(f"Output:\n {ret}\n")
    return ret

def main():
    pass

if __name__ == '__main__':
    main()
