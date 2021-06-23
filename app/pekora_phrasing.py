# -*- coding: utf-8 -*-

# Modules
import json

json_path = './json_folder/'
with open(json_path+"phrasing.json") as f:
    phrasing_json = json.load(f)

def introduce_pekora_phrasing(sentence):
    for s in list(phrasing_json):
        sentence=sentence.replace(s, phrasing_json[s])
    return sentence


sentence = """
こんにちは！わたしは君をまってた！違うか？
あなたたち、わたしのこと知りませんか
"""

if __name__ == "__main__":
    print(introduce_pekora_phrasing(sentence))
