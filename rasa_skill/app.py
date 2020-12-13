from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__, template_folder='Templates')
context_set = ""


@app.route("/", methods=['POST', 'GET'])
def main():
    return "Visa skill homepage"


@app.route("/visa", methods=['POST'])
def visa():
    card = {}
    buttons = []
    text = ""
    if request.json['session']['new']:
        val = "Привет."
        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
        if not res.ok:
            print(res.content)
        res = res.json()
        print(res)
        text = res[0]['text']
    elif request.json['request']['command'] == 'on_interrupt':
        text = "Пока. \nПриходи, когда поедешь в другую страну."
    else:
        val = request.json['request']['command']
        data = json.dumps({"sender": "Rasa", "message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
        res = res.json()
        print(res)
        text = res[0]['text']

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
