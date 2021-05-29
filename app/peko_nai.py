from mecab_operation import mecab_dict, Keitaiso

def exchange_pekonai(sentence):

    word_dict = mecab_dict(sentence)
    keitaiso=Keitaiso(word_dict)

    s_list = []
    LAST = len(word_dict)-1
    i=0
    while i <= LAST:

        # 変数の格納
        word0, form0 = keitaiso.get(i, word=True, form=True)
        if i != LAST:
            word1, form1 = keitaiso.get(i+1, word=True, form=True)

        # 条件に合致したら、ぺこらフレーズをいれる
        if word0 == "ない" and word1 == "の":
            s_list.append("ねぇー")
            i += 1

        elif word0 == "ない" and word1 == "か":
            s_list.append("ねぇーの")
            i += 2

        elif word0 in ["違う", "ちがう"] and word1 == "の":
            s_list.append("ちげぇー")
            i += 1

        elif word0 in ["違う", "ちがう"] and word1 == "の":
            s_list.append("ちげぇーの")
            i += 2

        # 条件に合致しなかったら、進む
        else:
            s_list.append(word0)
            i += 1

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
