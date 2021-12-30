import os
import sys

from dotenv import load_dotenv
from flask import Flask, request, abort, send_file
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=["user", "play1", "play2", "play3", "play4", "read1", "read2", "read3", "read4"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "play1",
            "conditions": "play",
        },
        {
            "trigger": "advance",
            "source": "play1",
            "dest": "play2",
            "conditions": "play",
        },
        {
            "trigger": "advance",
            "source": "play2",
            "dest": "play3",
            "conditions": "play",
        },
        {
            "trigger": "advance",
            "source": "play3",
            "dest": "play4",
            "conditions": "play",
        },
        {
            "trigger": "advance",
            "source": "play4",
            "dest": "play4",
            "conditions": "play",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "read1",
            "conditions": "read",
        },
        {
            "trigger": "advance",
            "source": "read1",
            "dest": "read2",
            "conditions": "read",
        },
        {
            "trigger": "advance",
            "source": "read2",
            "dest": "read3",
            "conditions": "read",
        },
        {
            "trigger": "advance",
            "source": "read3",
            "dest": "read4",
            "conditions": "read",
        },
        {
            "trigger": "advance",
            "source": "read4",
            "dest": "read4",
            "conditions": "read",
        },
        {
            "trigger": "advance",
            "source": ["user", "play1", "play2", "play3", "play4", "read1", "read2", "read3", "read4"],
            "dest": "user",
            "conditions": "reset",
        },
        {
            "trigger": "advance",
            "source": ["play1", "play2", "play3", "play4"],
            "dest": "read1",
            "conditions": "read",
        },
        {
            "trigger": "advance",
            "source": ["read1", "read2", "read3", "read4"],
            "dest": "play1",
            "conditions": "play",
        },

    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if not response:
            send_text_message(event.reply_token, "Please input the correct command!")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    show_fsm()
