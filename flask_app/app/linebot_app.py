import sys
import json
from pathlib import Path
from datetime import datetime as dt
import os
from flask import Flask, abort, request, render_template
from dotenv import load_dotenv
import scripts.functions as fcs
from linebot import (
    LineBotApi
)
from linebot.v3.webhook import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import pytz
jst = pytz.timezone('Asia/Tokyo')

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
UTIL_PATH = SCRIPT_DIR.parent.parent / 'utils'
CHECK_IP_PATH = UTIL_PATH / 'check_ip'
sys.path.append(str(UTIL_PATH))
from check_ip import check_ip
ENV_DIR = SCRIPT_DIR.parent.parent / '.env'

load_dotenv(str(ENV_DIR))

app = Flask(__name__)


INTERFACE      = os.getenv("INTERFACE")
ACCESS_TOKEN   = os.getenv("ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")


handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=ACCESS_TOKEN)


@app.route('/')
def hello():
   name = "Flask Hello World"
   return name


@app.route('/welcome', methods=['GET'])
def welcome():
   name = request.args.get('name', 'guest')
   print(name)
   msg = f"Hello, {name.upper()}!!"
   return msg

@app.route("/test", methods=['GET', 'POST'])
def test():
   return 'I\'m alive!'

@app.route("/message_test", methods=['GET'])
def message_test():
   return render_template('app/message_test.html')

@app.route("/send_test", methods=['POST'])
def send_test():
   msg = request.form['message']
   ret_msg = fcs.create_responce(msg)
   ret_msg = ret_msg.replace('\n', '<br>')
   return ret_msg


@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']

   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)

   # handle webhook body
   try:
      handler.handle(body, signature)
   except InvalidSignatureError:
      app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
      abort(400)

   return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
   print('message is received')
   input_msg = event.message.text

   # 受信したテキストの保存
   now = dt.now(jst).strftime("%Y-%m-%d %H:%M:%S")
   log_file = "/home/ubuntu/line-bot/log.txt"
   with open(log_file, 'a', encoding='utf-8') as f:
      f.write(f"[Time: {now}]\n")
      f.write(input_msg + '\n')

   with ApiClient(configuration) as api_client:
      output_msg = fcs.create_responce(input_msg)

      line_bot_api = MessagingApi(api_client)
      line_bot_api.reply_message_with_http_info(
         ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=output_msg)]
         )
      )
      with open(log_file, 'a', encoding='utf-8') as f:
         f.write(output_msg + '\n')

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port="8000", debug=True) # for debug
    app.run()
