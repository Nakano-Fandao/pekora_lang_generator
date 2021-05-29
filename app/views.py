# app.py
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
            'th': [],
            'td': [],
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': []
        }
    }
    """

    print('Request received from client')
    json_data = request.json

    body_dict = json_data['body']
    headline_dict = json_data['headline']

    # Translate the text one by one to Pekora lang (list → list)
    peko_body = list(map(translate_body, body_dict['p']))
    print("Pekora translation completed for Body sentences")

    peko_head = {}
    for headline_tag in headline_dict:
        peko_head[headline_tag] = list(map(translate_headline, headline_dict[headline_tag]))
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


def translate_body(sentence):
    peko_sentence = peko_lang.peko_main(sentence)
    return peko_sentence

def translate_headline(item):
    peko_item = peko_lang.peko_main(item)
    return peko_item


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
