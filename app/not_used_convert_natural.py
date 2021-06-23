# -*- coding: utf-8 -*-

# Modules
import json
from icecream import ic
from mecab_operation import Keitaiso

# Mode
debug = False

# Json Files
json_path = './json_folder/'
with open(json_path+"sonkei_kenjou.json") as f:
    sonken_json = json.load(f)

def convert_natural_to_peko(word_class):

    def normal_peko_translate(word):
        if word in ["だ"]:
            add_word = "ぺこ"
        else:
            add_word = word + "ぺこ"
        return add_word

    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    sentence = ""

    for i, word_dict in enumerate(word_class):

        word0, form0, kana0 = keitaiso.get(i, word=True, form=True, kana=True)
        if i != LAST: word1, part1, kana1 = keitaiso.get(i+1, word=True, part=True, kana=True)

        if form0 in ['終止形', "命令形"]:
            if i != LAST:
                if kana1 in ["カ", "ノ"]:
                    sentence += word0
                elif part1 in ["助動詞"]:
                    sentence += word0
                elif (kana1 == "ガ") & (word_class[i+1]['subpart1'] == "接続助詞"):
                    sentence += word0 + "けど"
                else:
                    sentence += normal_peko_translate(word0)
            else:
                sentence += normal_peko_translate(word0)
            continue

        elif (form0 in ["連体形"]) & (i != LAST):
            if word1 == "<":
                sentence += normal_peko_translate(word0)
                continue

        elif (kana0 in ['カ', 'ノ']) & (word_dict['subpart1'] == "終助詞"):
            sentence += "ぺこ"
            continue

        elif (kana0 == "ガ"):
            if sentence[-2:] == "けど":
                continue

        sentence += word0

    return sentence

if __name__ == '__main__':
    debug = True
    convert_natural_to_peko("word_class")
