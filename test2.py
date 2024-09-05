import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

with open('data/appliances_data.json', 'r', encoding='utf-8') as json_open:
    consumer_electronics = json.load(json_open)

def get_appropriate_element(input_message: str, list: str) -> str:
    prompt = f"以下の配列の中から、'{input_message}'に最も近い意味の要素を選んで出力してください。理由などは述べずに、推測した要素をそのまま出力してください。\n\n{list}"
    response = model.generate_content(prompt)
    return response.text


def create_message_from_json(question: str, json_data: str) -> str:
    prompt = f"以下のjsonファイルを学習して質問に答えてください。\n\n{json_data}\n\n質問:{question}"
    response = model.generate_content(prompt)
    return response.text

print(create_message_from_json('パソコンのプライスは？？', consumer_electronics))
