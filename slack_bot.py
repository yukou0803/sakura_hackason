import os
import json
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

json_open = open('data/appliances_data.json', 'r')
consumer_electronics = json.load(json_open)

def create_message_from_json(question: str, json_data: str) -> str:
    prompt = f"以下のjsonファイルを学習してplain textで質問に答えてください。\
        理由などは述べずに、推測した要素をそのまま出力してください。\
        該当するデータが含まれていない場合は、「データベースに~~に関する情報は含まれていません」を返してください。\
        製品名を答える時は「商品名(家電の種類)」の形式で答えてください。\
        回答する際には単位をつけてください。\
        \n\n{json_data}\n\n質問:{question}"
    response = model.generate_content(prompt)
    return response.text

@app.event("app_mention")  # chatbotにメンションが付けられたときのハンドラ
def respond_to_mention(event, say):
    text = re.sub(r'^<.*>', '', event['text'])
    say(create_message_from_json(text, consumer_electronics), mrkdwn=True)


@app.event("message") # ロギング
def handle_message_events(body, logger):
    logger.info(body)
    
SocketModeHandler(app, SLACK_APP_TOKEN).start()
