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
    text = ""
    if request.json['session']['new']:
        text = "Привет это скилл Виза"
    elif request.json['request']['command'] == 'on_interrupt':
        text = "Пока, возвращайся, когда отправишься в другую страну."
    elif request.json['request']['command'].lower() == 'привет' or request.json['request']['original_utterance'].lower() == 'привет':
        text = "Здравствуйте."
    elif request.json['request']['command'].lower() == 'картинка':
        text = ""
        card = {
        "type": 'BigImage',
        "image_id": 457239017,
        "title": "Красота",
        "description": ""

        }
    elif request.json['request']['command'].lower() == 'карусель' or request.json['request']['command'].lower() == 'картинки' or request.json['request']['command'].lower() == 'много картинок':
        card = {
        "type": 'ItemsList',
        "items": [
                {
                    "image_id": 457239018
                }, 
                {
                    "image_id": 457239019
                },
                {
                    "image_id": 457239017
                }
            ]
        }
    elif request.json['request']['command'].lower() == 'кнопки':
        buttons = [
            {
                "title": "Австрия"
            },
            {
                "title": "Бельгия"
            },
            {
                "title": "Чешская Республика"
            },
            {
                "title": "Дания"
            },
            {
                "title": "Эстония"
            },
            {
                "title": "Финляндия"
            },
            {
                "title": "Франция"
            },
            {
                "title": "Германия"
            },
            {
                "title": "Греция"
            },
            {
                "title": "Венгрия"
            },
            {
                "title": "Исландия"
            },
            {
                "title": "Италия"
            },
            {
                "title": "Латвия"
            },
            {
                "title": "Литва"
            },
            {
                "title": "Люксембург"
            },
            {
                "title": "Мальта"
            },
            {
                "title": "Голландия"
            },
            {
                "title": "Норвегия"
            },
            {
                "title": "Польша"
            },
            {
                "title": "Португалия"
            },
            {
                "title": "Словакия"
            },
            {
                "title": "Словения"
            },
            {
                "title": "Испания"
            },
            {
                "title": "Швеция"
            },
            {
                "title": "Швейцария"
            },
            {
                "title": "Лихтенштейн"
            }
        ]
    elif request.json['request']['command'].lower() == 'австрия':
        text = "В Австрию нужна шенгенская виза."
    else:
        text = "не понимаю"

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        'response': {
            "end_session":False,
            "text": text,
            "card": card,
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