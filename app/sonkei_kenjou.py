# -*- coding: utf-8 -*-

# Modules
import json
from icecream import ic
from katsuyou import get_katsuyou
from mecab_operation import mecab_dict, Keitaiso

# Mode
debug = False

# Json Files
json_path = './json_folder/'
with open(json_path+"polite.json") as f:
    polite_json = json.load(f)

# 尊敬語・謙譲語を除去
def remove_sonken(sentence):
    """
        p_word1:    previous keitaiso
        word0:      current keitaiso
        word1:      next keitaiso
    """

    word_class = mecab_dict(sentence)
    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    s_list = []
    action_word = ""
    katsuyou_flag = False
    skip = False

    # 関数
    add = s_list.append
    pop = s_list.pop

    for i in range(LAST+1):

        #* 形態素情報を格納-----------------------------------------
        word0, part0, subpart0, form0, kana0 = keitaiso.get(i, word=True, part=True, subpart1=True, form=True, kana=True)

            # 最後以外
        if i < LAST:
            word1, part1, type1, origin1, kana1 = keitaiso.get(i+1, word=True, part=True, type=True, origin=True, kana=True)
            if i < LAST - 1:
                [kana2] = keitaiso.get(i+2, kana=True)
            else:
                kana2 = None

            # 最後は、次の形態素情報にNoneを格納
        else:
            word1, part1, type1, origin1, kana1 \
                = [None]*5

        # デバッグ時の確認
        if debug: ic(word0, part0, subpart0, form0, kana0)
        #* --------------------------------------------------------

        if skip:
            if kana0 == action_word:
                if katsuyou_flag:
                    form0 = katsuyou_flag
                    katsuyou_flag = False

                # 「た」に繋がるため音便あり
                onbin = (False, True) [kana1 in ['タ']]
                add(get_katsuyou(n_origin, n_type, form0, onbin))
                skip = False
            continue

        elif katsuyou_flag:
            add(get_katsuyou(n_origin, n_type, katsuyou_flag, False))
            katsuyou_flag = False
            continue

        #* Main----------------------------------------------------
        elif (part0 == "接頭辞") & (kana0 in ["オ", "ゴ"]):

            if part1 == "動詞":
                if kana1 in polite_json:
                    n_origin = polite_json[kana1]['常体']
                    n_type = polite_json[kana1]["段-行"]

                # "お買いになる"などセットで尊敬・謙譲語になるもの
                else:
                    n_origin = origin1
                    n_type = type1

                if i == LAST-1:
                    katsuyou_flag = "命令形"
                    continue

                elif i < LAST-1:
                    skip = True
                    if kana2 == "クダサル":
                        add(word1)
                        add("て")
                        n_origin = "くれる"
                        n_type = "下一段-ラ行"
                        action_word = kana2

                    elif kana2 == "イタス":
                        action_word = kana2

                    elif kana2 != 'ニ':
                        skip = False
                        katsuyou_flag = "命令形"

                    elif i < LAST-2:
                        if (kana2 == "ニ") & (word_class[i+3]['kana'] == "ナル"):
                            action_word = "ナル"

                continue

            elif part1 == "名詞":

                if kana1 in ["カケ", "メシ"]:
                    n_origin = polite_json[kana1]['常体']
                    n_type = polite_json[kana1]['段-行']
                    skip = True

                    if kana2 == "ニ":
                        if i < LAST - 2:
                            if word_class[i+3]['kana'] == "ナル":
                                action_word = "ナル"
                                continue
                        action_word = "ニ"
                        katsuyou_flag = "命令形"

                    elif kana2 == "クダサル":
                        action_word = "クダサル"

                    else:
                        action_word = word1
                        katsuyou_flag = "命令形"

                    continue

        elif (part0 == "名詞") & (kana0 in ["ゴラン"]):
                    n_origin = polite_json[kana0[1:]]['常体']
                    n_type = polite_json[kana0[1:]]['段-行']

                    if i == LAST:
                        add(get_katsuyou(n_origin, n_type, "命令形", False))

                    elif kana1 == "クダサル":
                        print('hi')
                        skip = True
                        action_word = "クダサル"

                    elif i < LAST-1:
                        if (kana1 == "ニ") & (kana2 == "ナル"):
                            skip = True
                            action_word = "ナル"
                        elif kana1 == 'ニ':
                            skip = True
                            action_word = "ニ"
                            katsuyou_flag = "命令形"
                        else:
                            add(get_katsuyou(n_origin, n_type, "命令形", False))

                    continue

        elif part0 == "動詞":

            if i == LAST:
                kana1 = None
            else:
                # 「た」に繋がるため音便あり
                onbin = (False, True) [kana1 in ['タ']]

            if kana0 in polite_json:
                if kana1 in ["アゲル"]:
                    n_origin = polite_json[kana0+kana1]['常体']
                    n_type = polite_json[kana0+kana1]['段-行']
                    skip = True
                    action_word = 'アゲル'
                else:
                    add(get_katsuyou(polite_json[kana0]['常体'], polite_json[kana0]['段-行'], form0, onbin))
                    continue

        elif part0 == "助動詞":

            # 「た」に繋がるため音便あり
            onbin = (False, True) [kana1 in ['タ']]

            if kana0 in ["テラッシャル"]:
                original_json = polite_json[kana0]
                add(get_katsuyou(original_json['常体'], original_json['段-行'], form0, onbin))
                continue

        add(word0)

    return ''.join(s_list)

if __name__ == '__main__':
    sentence = """君はありがとうと言った。
    助けてくれると嬉しい。
    """

    debug = True
    remove_sonken(sentence)
