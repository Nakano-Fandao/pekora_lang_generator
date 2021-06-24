# -*- coding: utf-8 -*-

# Modules
from icecream import ic
from mecab_operation import mecab_dict, Keitaiso

#Mode
debug = False

def add_peko(sentence):
    """
        word0:      current keitaiso
        word1:      next keitaiso
    """

    word_class = mecab_dict(sentence)
    keitaiso = Keitaiso(word_class)
    LAST = len(word_class)-1
    s_list = []
    skip = 0

    # 関数
    add = s_list.append

    # 文字を最初からしらべてぺこを挿入
    for i in range(LAST+1):

        # skip処理
        if skip > 0: skip-= 1; continue

        # 変数を格納
        word0, part0, subpart0, form0, origin0 = keitaiso.get(i, word=True, part=True, subpart1=True, form=True, origin=True)

        if i < LAST:
            word1, part1, form1 = keitaiso.get(i+1, word=True, part=True, form=True)
            if i < LAST-1:
                word2, part2 = keitaiso.get(i+2, word=True, part=True)
            else:
                word2 = None
                part2 = '補助記号'
        else:
            word1 = None
            form1 = None
            part1 = '補助記号'

        # デバッグ時の形態素確認
        if debug: ic(word0, part0, subpart0, form0, origin0)

        # 黙れ > 黙れぺこ
        if form0 == "命令形":
            add(origin0)
            add("ぺこ")
            continue

        # 寝る。 > 寝るぺこ。
        elif form0 == "終止形":
            add(word0)
            add("ぺこ")
            continue

        # 終わりにする？ > 終わりにするぺこ？
        elif (form0 == "連体形"):
            add(word0)
            if (word1 == "の") & (part1 == "助詞"):
                add("ぺこなの")
                skip = 1; continue
            elif (part1 in ["補助記号"]):
                add("ぺこ")
                continue
            elif (part1 in ["名詞"]):
                continue
            else:
                continue

        # マリンか？ > マリンぺこか？
        elif (word0 == "か") & (part1 == "補助記号"):
            continue

        elif (part0 == "名詞"):
            # おばけか > おばけぺこか
            if (word1 == 'か'):
                add(word0)
                add("ぺこ")
                skip = 1; continue

            # 配信だが > 配信ぺこなんですけど
            elif (word1 == "だ") & (form1 == "終止形"):
                add(word0)
                add("ぺこ")
                if (word2 == "が") & (part2 == "助詞"):
                    add("なんですけど")
                    skip = 2; continue
                else:
                    skip = 1; continue

        #　嘘じゃん > 嘘ぺこじゃん
        elif subpart0 in ["終助詞"]:
            add("ぺこ")
            add(word0)
            continue

        # 条件に引っかからなかったら
        add(word0)
        continue

    peko_sentence = ''.join(s_list)

    return peko_sentence


sentence = """お手数おかけしますって英語でなんて言うの？
お手数おかけしてすみませんって英語でなんて言うの？
全国で発売って英語でなんて言うの？
歴史上の人物って英語でなんて言うの？
図書館で借りてきた教則本を見ながら(ピアノを)練習したって英語でなんて言うの？
不明な点がございましたらスタッフまでお声がけ下さい。って英語でなんて言うの？
彼に甘やかしすぎではないですか？って英語でなんて言うの？
準決勝進出４チームが出揃いました って英語でなんて言うの？
彼女を操るような真似するなって英語でなんて言うの？
"""

if __name__ == "__main__":
    debug = True
    print(add_peko(sentence))
