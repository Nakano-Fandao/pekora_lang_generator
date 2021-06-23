# -*- coding: utf-8 -*-

# Modules
import json
from icecream import ic
from mecab_operation import Keitaiso
from katsuyou import get_katsuyou

# Mode
debug = False

# Json Files
json_path = './json_folder/'
with open(json_path+"sonkei_kenjou.json") as f:
    sonken_json = json.load(f)

# 尊敬語・謙譲語を除去
def remove_sonken(word_class):
    """
        p_word1:    previous keitaiso
        word0:      current keitaiso
        word1:      next keitaiso
    """

    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    sentence = ""
    action_word = ""
    katsuyou_flag = False
    skip_flag = False

    for i, word_dict in enumerate(word_class):

        # 形態素の情報を取得
        word0, part0, subpart0, form0, kana0 = keitaiso.get(i, word=True, part=True, subpart0=True, form=True, kana=True)

            # 最後以外
        if i < LAST:
            word1, part1, type1, origin1, kana1 = keitaiso.get(i+1, word=True, part=True, type=True, origin=True, kana=True)
            if i < LAST - 1:
                kana2 = keitaiso.get(i+2, kana=True)[0]
            else:
                kana2 = None

            # 最後は、次の形態素情報にNoneを格納
        else:
            word1, part1, type1, origin1, kana1 \
                = [None]*5


        # デバッグ時の確認
        if debug: ic(word0, part0, subpart0, form0, kana0)

        if skip_flag:
            if kana0 == action_word:
                if katsuyou_flag:
                    form0 = katsuyou_flag
                    katsuyou_flag = False

                # 「た」に繋がるため音便あり
                onbin = (False, True) [kana1 in ['タ']]
                sentence += get_katsuyou(natural_origin, natural_type, form0, onbin)
                skip_flag = False
            continue

        elif katsuyou_flag:
            sentence += get_katsuyou(natural_origin, natural_type, katsuyou_flag, False)
            katsuyou_flag = False
            continue

        elif (part0 == "接頭辞") & (kana0 in ["オ", "ゴ"]):

            if part1 == "動詞":
                if kana1 in sonken_json:
                    natural_origin = sonken_json[kana1]['常体']
                    natural_type = sonken_json[kana1]["段-行"]

                # "お買いになる"などセットで尊敬・謙譲語になるもの
                else:
                    natural_origin = origin1
                    natural_type = type1

                if i == LAST-1:
                    katsuyou_flag = "命令形"
                    continue

                elif i < LAST-1:
                    skip_flag = True
                    if kana2 in ["クダサル", "イタス"]:
                        action_word = kana2

                    elif kana2 != 'ニ':
                        skip_flag = False
                        katsuyou_flag = "命令形"

                    elif i < LAST-2:
                        if (kana2 == "ニ") & (word_class[i+3]['kana'] == "ナル"):
                            action_word = "ナル"

                continue

            elif part1 == "名詞":

                if kana1 in ["カケ", "メシ"]:
                    natural_origin = sonken_json[kana1]['常体']
                    natural_type = sonken_json[kana1]['段-行']
                    skip_flag = True

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
                    natural_origin = sonken_json[kana0[1:]]['常体']
                    natural_type = sonken_json[kana0[1:]]['段-行']

                    if i == LAST:
                        sentence += get_katsuyou(natural_origin, natural_type, "命令形", False)

                    elif kana1 == "クダサル":
                        skip_flag = True
                        action_word = "クダサル"

                    elif i < LAST-1:
                        if (kana1 == "ニ") & (kana2 == "ナル"):
                            skip_flag = True
                            action_word = "ナル"
                        elif kana1 == 'ニ':
                            skip_flag = True
                            action_word = "ニ"
                            katsuyou_flag = "命令形"
                        else:
                            sentence += get_katsuyou(natural_origin, natural_type, "命令形", False)

                    continue

        elif part0 == "動詞":

            if i == LAST:
                kana1 = None
            else:
                # 「た」に繋がるため音便あり
                onbin = (False, True) [kana1 in ['タ']]

            if kana0 in sonken_json:
                if kana1 in ["アゲル"]:
                    natural_origin = sonken_json[kana0+kana1]['常体']
                    natural_type = sonken_json[kana0+kana1]['段-行']
                    skip_flag = True
                    action_word = 'アゲル'
                else:
                    sentence += get_katsuyou(sonken_json[kana0]['常体'], sonken_json[kana0]['段-行'], form0, onbin)
                    continue

        elif part0 == "助動詞":

            # 「た」に繋がるため音便あり
            onbin = (False, True) [kana1 in ['タ']]

            if kana0 in ["テラッシャル"]:
                original_json = sonken_json[kana0]
                sentence += get_katsuyou(original_json['常体'], original_json['段-行'], form0, onbin)
                continue

        sentence += word0

    return sentence

if __name__ == '__main__':
    debug = True
    remove_sonken("word_class")
