# -*- coding: utf-8 -*-

# Modules
import MeCab

# MeCab data → list of dictionary
def mecab_dict(text):
    tagger = MeCab.Tagger()
    tagger.parse('')
    tagger.parseToNode('dummy')
    node = tagger.parseToNode(text)
    word_class = []
    """
    word_class
    {   "word": 形態素,
        "part": 品詞,
        "subpart1": 品詞細分類1（普通名詞、格助詞、非自立可能など）,
        "subpart2": 品詞細分類2（一般など）,
        "type": 活用形（五段-ラ行、助動詞-タなど）,
        "form": 活用型（連用形-イ音便、終止形-一般など）,
        "origin": 原型 ,
        "kana": カナ    }
    """
    while node:
        word = node.surface
        wclass = node.feature.split(',')
        if wclass[0] != 'BOS/EOS':
            # 日本語のとき
            try:
                word_class.append({"word": word, "part": wclass[0], "subpart1": wclass[1], "subpart2": wclass[2], "type": wclass[4], "form": wclass[5].split('-')[0], "origin": wclass[10], "kana": wclass[11]})
            # 英語のとき
            except:
                word_class.append({"word": word, "part": wclass[0], "subpart1": wclass[1], "subpart2": wclass[2], "type": wclass[4], "form": wclass[5].split('-')[0], "origin": "", "kana": ""})
        node = node.next
    return word_class


class Keitaiso():

    def __init__(self, word_class):
        self.word_class = word_class

    # Get details of keitaiso
    def get(self, index, **bool_dict):
        keitaiso_list = [val for key, val in self.word_class[index].items() if bool_dict.get(key)]
        return keitaiso_list
