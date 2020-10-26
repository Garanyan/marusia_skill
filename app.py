import json
import logging
from flask import Flask, request

app = Flask(__name__)


@app.route("/marusya", methods=["POST", "GET"])
def marusya():
    return "Marusya"

@app.route("/visa", methods=['POST'])
def visa():
    card = {}
    buttons = []
    text = "эх"
    if request.json['session']['new']:
        text = "Привет это скилл Виза"
    elif request.json['request']['command'] == 'on_interrupt':
        text = "Пока, возвращайся, когда отправишься в другую страну."
    elif request.json['request']['command'].lower() == 'привет' or request.json['request']['original_utterance'].lower() == 'привет':
        text = "Здравствуйте."
    elif request.json['request']['command'].lower() == 'картинка':
        card = {
        "type": 'BigImage',
        "image_id": 457239017,
        "title": "Красота",
        "description": ""

        }
    elif request.json['request']['command'].lower() == 'карусель':
        card = {
        "type": 'ItemsList',
        "items": [457239018, 457239019, 457239017],
        "title": "",
        "description": ""
        }
    elif request.json['request']['command'].lower() == 'кнопки':
        buttons = [
              {
                "title": "1"
              },
              {
                "title": "2"
              },
              {
                "title": "3"
              }
        ]


    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        'response':{
            "end_session":False,
            "text":text,
            "card":card,
            "buttons": buttons
        }
    }
    return json.dumps(response, ensure_ascii=False)

@app.route("/")
def home():
    return "Welcome page!"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)