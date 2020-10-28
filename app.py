import json
import logging
from flask import Flask, request

app = Flask(__name__)


def isSchengenArea(country):
    if country in ["австрия", "бельгия", "чешская республика", "чехия", "дания", "эстония", "финляндия", "франция",
                   "германия",
                   "греция", "венгрия", "исландия", "италия", "латвия", "литва", "люксембург", "мальта", "голландия",
                   "норвегия", "польша", "португалия", "словакия", "словения", "испания", "швеция", "швейцария",
                   "лихтенштейн"]:
        return True

    return False


def isNoVisaForRussians(country):
    counties_documents = {
        "белоруссия": "до 90 дней нужен паспорт гражданина РФ или нужен загранпаспорт",
        "босния и герцеговина": "до 30 дней  нужен загранпаспорт, действительный на момент въезда; обратные билеты и документы, подтверждающие платёжеспособность",
        "маке": "дония  до 90 дней  нужен загранпаспорт; страховка",
        "молдавия": "до 90 дней  нужен загранпаспорт; плюс необходимо зарегистрироваться в «Бюро миграции и убежища» или в «CRIS Registru» в течение 72 часов",
        "сербия": "до 30 дней  нужен загранпаспорт, действительный всё время поездки",
        "турция": "до 60 дней  нужен загранпаспорт сроком действия не менее 6 месяцев; иногда — туристический ваучер и обратные билеты",
        "украина": "до 90 дней  нужен загранпаспорт; иногда — обратные билеты, документы, подтверждающие платёжеспособность и приглашение принимающей стороны; есть ограничения на въезд для мужчин призывного возраста",
        "черногория": "до 30 дней  нужен загранпаспорт; плюс в течение суток необходимо оформить регистрацию",
        "абхазия": "до 90 дней нужен паспорт гражданина РФ или нужен загранпаспорт",
        "азербайджан": "до 90 дней  нужен загранпаспорт, действительный всё время поездки",
        "армения": "до 180 днейнужен паспорт гражданина РФ или нужен загранпаспорт",
        "бангладеш": "до 15 дней (и только в аэропорту Дакки) нужен загранпаспорт, обратный билет; заполненная миграционная карточка; обратный билет с фиксированной датой; взнос наличными 50 долларов.",
        "бруней": "до 14 дней  нужен загранпаспорт с запасом в шесть месяцев на дату пересечения границы; обратный билет",
        "восточный тимор / тимор-лесте": "до 30 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент въезда; подтверждение платёжеспособности; бронь отеля; сбор 30 долларов наличными",
        "вьетнам": "до 15 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент выезда; обратные билеты",
        "гонконг": "до 14 дней  нужен загранпаспорт сроком действия не менее месяца с момента выезда; обратные билеты; документы, подтверждающие платёжеспособность",
        "грузия": "до 1 года  нужен загранпаспорт, действительный всё время поездки",
        "израиль": "до 90 дней  нужен загранпаспорт сроком действия не менее 6 месяцев; билеты с закрытыми датами; страховка;  бронь в отеле; документы, подтверждающие платёжеспособность;",
        "индонезия": "до 30 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент выезда",
        "иордания": "до 30 дней  нужен загранпаспорт; сбор в 40 иорданских динаров (около 57 долларов)",
        "киргизия": "до 30 дней нужен паспорт гражданина РФ или нужен загранпаспорт",
        "казахстан": "до 30 дней нужен паспорт гражданина РФ или нужен загранпаспорт",
        "камбоджа": "до 30 дней  нужен загранпаспорт",
        "лаос": "до 15 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент поездки; иногда могут спросить обратные билеты и подтверждение материального благосостояния",
        "макао": "до 30 дней  нужен загранпаспорт; обратные билеты; бронь отеля; документы, подтверждающие платёжеспособность; миграционная карта (обычно их раздают в самолёте); сбор в 100 MOP (около 800 рублей)",
        "малайзия": "до 30 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент въезда; билеты; документы, подтверждающие платёжеспособность",
        "мальдивы": "до 30 дней  нужен загранпаспорт; билеты; подтверждение брони в отеле",
        "монголия": "до 30 дней  нужен загранпаспорт, действительный на момент въезда",
        "оаэ": "до 30 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент въезда",
        "таджикистан": "до 90 дней нужен паспорт гражданина РФ или нужен загранпаспорт; таможенная декларация; миграционная карта",
        "таиланд": "до 30 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент въезда; миграционная карта; обратные билеты; документы, подтверждающие платёжеспособность",
        "узбекистан": "до 60 дней  нужен загранпаспорт, действительный всё время поездки",
        "филиппины": "до 30 дней  нужен загранпаспорт сроком действия не менее 6 месяцев на момент въезда; обратные билеты; документы, подтверждающие платёжеспособность",
        "южная корея": "до 60 дней  нужен загранпаспорт, действительный на момент въезда; обратные билеты; документы, подтверждающие платёжеспособность; миграционная карта и таможенная декларация (выдаются в самолёте)",
        "южная осетия": "до 90 дней нужен паспорт гражданина РФ или нужен загранпаспорт"
    }
    if country in counties_documents:
        return counties_documents[country]

    return ""


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
    elif request.json['request']['command'].lower() == 'привет' or request.json['request'][
        'original_utterance'].lower() == 'привет':
        text = "Здравствуйте."
    elif request.json['request']['command'].lower() == 'картинка':
        text = ""
        card = {
            "type": 'BigImage',
            "image_id": 457239017,
            "title": "Красота",
            "description": ""

        }
    elif request.json['request']['command'].lower() == 'карусель' or request.json['request'][
        'command'].lower() == 'картинки' or request.json['request']['command'].lower() == 'много картинок':
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
    elif isSchengenArea(request.json['request']['command'].lower()):
        text = f"В {request.json['request']['command'].lower()} нужна шенгенская виза."
    elif isNoVisaForRussians(request.json['request']['command'].lower()):
        text = f"Для посещения {request.json['request']['command']} россиянам не нужна виза. Можно находиться " + isNoVisaForRussians(
            request.json['request']['command'].lower())
    else:
        text = "не понимаю"

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        'response': {
            "end_session": False,
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
