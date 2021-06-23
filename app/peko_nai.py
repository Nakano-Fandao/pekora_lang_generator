# -*- coding: utf-8 -*-

# Modules
from mecab_operation import mecab_dict, Keitaiso

def exchange_pekonai(sentence):

    word_dict = mecab_dict(sentence)
    keitaiso=Keitaiso(word_dict)

    s_list = []
    skip = 0
    LAST = len(word_dict)-1

    # 関数
    add = s_list.append

    for i in range(LAST+1):

        # skip処理
        if skip > 0: skip-= 1; continue

        # 変数の格納
        word0, form0 = keitaiso.get(i, word=True, form=True)
        if i != LAST:
            word1, form1 = keitaiso.get(i+1, word=True, form=True)

        # 条件に合致したら、ぺこらフレーズをいれる
        if word0 == "ない" and word1 == "の":
            add("ねぇー")
            continue

        elif word0 == "ない" and word1 == "か":
            add("ねぇーの")
            skip = 1
            continue

        elif word0 in ["違う", "ちがう"] and word1 == "の":
            add("ちげぇー")
            continue

        elif word0 in ["違う", "ちがう"] and word1 == "の":
            add("ちげぇーの")
            skip = 1
            continue

        # 条件に合致しなかったら、進む
        else:
            add(word0)
            continue

    peko_sentence = ''.join(s_list)

    return peko_sentence

sentence = """
知らないの？
知らないの。
食べないか？
食べないか
"""

if __name__ == "__main__":
    print(exchange_pekonai(sentence))
