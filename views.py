# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import json
app = Flask(__name__)
cors = CORS(app)

# トップページにアクセスされたらindex.htmlを表示する
@app.route('/')
def index():
    return render_template("test.html")

# /pekoraにPOSTリクエストが送られたら処理してJSONを返す
@app.route('/pekora', methods=['POST'])
def pekora():
    """
    Expected data format is json of dict below:
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
    }
    """

    print('Request received from client')
    json_data = request.json

    body_dict = json_data['body']
    headline_dict = json_data['headline']

    # Translate the text one by one to Pekora lang (list → list)
    peko_body = list(map(translate_body, body_dict['p']))
    peko_head = translate_headline(headline_dict)

    peko_dict = {
        'body': {
            'p': peko_body
        },
        'headline': peko_head
    }

    peko_json = json.dumps(peko_dict)

    # send data to client 
    return jsonify(peko_json)


def translate_body(item):
    return item + 'ぺこ'

def translate_headline(item):
    return item


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)