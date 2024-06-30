import sys
import json
from pathlib import Path
import os
from flask import Flask, abort, request, jsonify
from dotenv import load_dotenv
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

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
UTIL_PATH = SCRIPT_DIR.parent.parent / 'utils'
CHECK_IP_PATH = UTIL_PATH / 'check_ip'
sys.path.append(str(UTIL_PATH))
from check_ip import check_ip
ENV_DIR = SCRIPT_DIR.parent.parent / '.env'

load_dotenv(str(ENV_DIR))

app = Flask(__name__)


INTERFACE = os.getenv("INTERFACE")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
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
    with ApiClient(configuration) as api_client:
        #相手の送信した内容で条件分岐して回答を変数に代入
        if event.message.text == 'ip':
            ip_address = check_ip()
            msg = 'パー'
        else:
            msg = 'ごめんね。\nまだ他のメッセージには対応してないよ'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

if __name__ == "__main__":
    app.run()
