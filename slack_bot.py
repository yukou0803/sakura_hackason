import os
import json
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


json_token = open('slack_token.json')
token = json.load(json_token)
SLACK_BOT_TOKEN = token["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = token["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

json_open = open('data/aappliances_data.json', 'r')
consumer_electronics = json.load(json_open)

# consumer_electronics = json_load["家電リスト"][0]
info = {}
# print(consumer_electronics)

@app.event("app_mention")  # chatbotにメンションが付けられたときのハンドラ
def respond_to_mention(event, say):
    text = re.sub(r'^<.*>', '', event['text'])
    # print(text)
    # print(text=="冷蔵庫")
    global info
    # text = event["text"]
    flag = 0
    for key in consumer_electronics:
        if key in text:
            flag = 1
            info = consumer_electronics[key]
            say(f"{key} に関して知りたい情報を教えてください")

    if flag == 0:
        say("指定された情報は見つかりませんでした。")


@app.message("価格")
def response_info(say):
    say(info["価格"])

@app.message("メーカー")
def response_info(say):
    say(info["メーカー"])

@app.message("機能")
def response_info(say):
    say(info["機能"])

@app.message("容量")
def response_info(say):
    say(info[""])

@app.message("サイズ")
def response_info(say):
    say(info["サイズ"])

@app.message("消費電力")
def response_info(say):
    say(info["消費電力"])

@app.message("重量")
def response_info(say):
    say(info["重量"])

@app.message("色")
def response_info(say):
    say(info["色"])

@app.message("保証期間")
def response_info(say):
    say(info["保証期間"])

@app.message("発売年")
def response_info(say):
    say(info["発売年"])

@app.message("耐久年数")
def response_info(say):
    say(info["耐久年数"])

@app.message("レビュー")
def response_info(say):
    say(info["レビュー"])


@app.message("hello")  # 送信されたメッセージ内に"hello"が含まれていたときのハンドラ
def response_info(say):
    say("can I help you?")

@app.event("message") # ロギング
def handle_message_events(body, logger):
    logger.info(body)
    
SocketModeHandler(app, SLACK_APP_TOKEN).start()
