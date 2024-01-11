from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "49ef3d6c1bd134fbca5c1ffb7b3b445b"
channel_access_token = "zl89CoWtORT7USUU6pO56mq9fdPKkrI8JiJsJ/qJis4jBYi2lJ2Gfk8HNzUb9WxPdJZfIaB/dantO1HFo921+kej3DcqXLU67157EVbJcGnIl+ZRXQBkd0vb8J6v3dJbMexFaoK5zsgUw9H1H7EiTAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass

    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()
