from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import os

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = SCRIPT_DIR.parent.parent.parent / '.env'
load_dotenv(str(ENV_DIR))
API_KEY = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key = API_KEY)
prompt = "日本の特徴について200字で説明してください。"
# model = "gpt-3.5-turbo"
model = "gpt-3.5-turbo"
response = client.chat.completions.create(
    model=model,
    messages = [
        {"role": "user", "content": prompt},
    ],
    max_tokens=500,
    temperature=0.3
)

print(response.choices[0].message.content)
