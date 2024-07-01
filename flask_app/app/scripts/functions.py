import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = SCRIPT_DIR.parent.parent.parent / '.env'
load_dotenv(str(ENV_DIR))
API_KEY = os.getenv("OPENAI_API_KEY")

def generate_text(msg, model):
    client = OpenAI(api_key = API_KEY)
    response = client.chat.completions.create(
        model=model,
        messages = [{"role": "user",
                     "content": msg}],
        max_tokens=500,
        temperature=0.3
    )
    ret = response.choices[0].message.content
    return ret


def main():
    msg = "ubuntuとは何ですか？"
    model = "gpt-3.5-turbo"
    print(generate_text(msg, model))

if __name__ == "__main__":
    main()
