# app.py
from os import terminal_size
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import peko_lang

app = Flask(__name__)
CORS(app)

# トップページにアクセスされたらindex.htmlを表示する
@app.route('/')
def index():
    return render_template("test.html")

# /pekoraにPOSTリクエストが送られたら処理してJSONを返す
@app.route('/pekora', methods=['POST'])
def pekora():
    """
    Expected data format is json of dict:
    {
        'body': {
            'p': []
        },
        'headline': {
            'li': [],
            ...
        }
    }
    """

    print('Request received from client')
    json_data = request.json

    body_dict = json_data['body']
    headline_dict = json_data['headline']

    # Translate the text one by one to Pekora lang (list → list)
    peko_body = translate_body(body_dict['p'])
    print("Pekora translation completed for Body sentences")

    peko_head = translate_headline(headline_dict)
    print("Pekora translation completed for Headlines and lists")

    peko_dict = {
        'body': {
            'p': peko_body
        },
        'headline': peko_head
    }

    peko_json = json.dumps(peko_dict)

    # send data to client
    return jsonify(peko_json)


def translate_body(sentence_list):
    peko_sentence_list = list(map(peko_lang.peko_main, sentence_list))
    return peko_sentence_list

def translate_headline(headline_dict):
    headline_numbers = [len(lines) for lines in headline_dict.values()]
    headline_values = sum(headline_dict.values(), [])

    peko_headlines = list(map(peko_lang.peko_main, headline_values))

    peko_head = {}
    for i, tag in enumerate(list(headline_dict)):
        peko_head[tag] = peko_headlines[0:headline_numbers[i]]
        del peko_headlines[0:headline_numbers[i]]

    return peko_head


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
