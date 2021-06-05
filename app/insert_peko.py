from mecab_operation import mecab_dict, Keitaiso

def add_peko(sentence):

    word_class = mecab_dict(sentence)
    keitaiso=Keitaiso(word_class)
    LAST = len(word_class)-1
    s_list = []

    i = 0
    while i <= LAST:

        # 変数を格納
        word0, part0, subpart0, form0, origin0 = keitaiso.get(i, word=True, part=True, subpart1=True, form=True, origin=True)

        if i != LAST:
            word1, part1 = keitaiso.get(i+1, word=True, part=True)
        elif i == LAST:
            word1 = None
            part1 = '補助記号'

        if word0 == "な":
            s_list.append(word0)
            s_list.append("ぺこ")
            i += 1

        elif form0 == "命令形":
            s_list.append(origin0)
            s_list.append("ぺこ")
            i += 1

        elif (form0 == "終止形") & (part1 in ["補助記号", "助詞"]):
            s_list.append(word0)
            s_list.append("ぺこ")
            i += 1

        elif (form0 == "連体形") & (part1 in ["補助記号"]):
            s_list.append(word0)
            s_list.append("ぺこ")
            i += 1

        elif (word0 == "か") & (part1 == "補助記号"):
            i += 1

        elif (part0 == "名詞") & (word1 == 'か'):
            s_list.append(word0)
            s_list.append("ぺこ")
            i += 2


        elif subpart0 in ["終助詞", "副助詞"]:
            s_list.append("ぺこ")
            s_list.append(word0)
            i += 1

        else:
            s_list.append(word0)
            i += 1

        # print(word0, part0, subpart0, form0)

    peko_sentence = ''.join(s_list)

    return peko_sentence


sentence = """
<ahref='#1'>ぺーこぺこぺこ</a>
"""

if __name__ == "__main__":
    print(add_peko(sentence))
