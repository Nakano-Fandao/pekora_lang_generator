# -*- coding: utf-8 -*-

# Modules
import json
from icecream import ic

# Mode
debug = False

# Constants
json_path = './json_folder/'
with open(json_path+"katsuyou.json") as f:
    katsuyou_json = json.load(f)


def get_katsuyou(origin, type, form, onbin):
    """
    dan   : 段（五段活用）  or 助動詞
    gyou  : 行（ア行）      or ダ
    form  : 形（終止形）
    onbin : True or False（True: 撥音便, イ音便, 促音便がある）
    root  : 語幹
    """

    # 動詞-変格活用 以外のとき（"五段-ア行" or "助動詞-ダ"）
    if '-' in type:
        dan, gyou = type.split('-')
        target_katsuyou = katsuyou_json[dan][gyou]

    else:
        # 動詞-変格活用のとき（"カ行変格"）
        try:
            dan = type
            target_katsuyou = katsuyou_json[dan]
        except:
            # 記号のときは、そのまま返す
            return origin

    if debug: ic(origin, type, form, onbin)

    if dan in ['五段']:

        root = origin.rsplit(target_katsuyou["終止形"][0])[0]
        if onbin:

            # 促音便-確定のとき
            if origin in ['行く', 'いく']:
                katsuyou = root + "っ"
            # ウ音便-確定のとき
            elif origin in ['問う', 'とう', '請う', '乞う', 'こう', '厭う', 'いとう']:
                katsuyou = root + "う"
            # その他
            else:
                katsuyou = root + target_katsuyou[form][1]

        elif not onbin:
            katsuyou = root + target_katsuyou[form][0]

    elif dan in ['上一段', '下一段', 'カ行変格', 'サ行変格']:

        # 〇老いる、〇いる
        if target_katsuyou["終止形"][0] in origin:
            root = origin.rsplit(target_katsuyou["終止形"][0])[0]
            katsuyou = root + target_katsuyou[form][0]
        # 活用に漢字が含まれているもの（居る、など）
        else:
            root = origin.rsplit(target_katsuyou["終止形"][0][-1])[0]
            katsuyou = root + target_katsuyou[form][0][1:]

    elif dan in ['助動詞']:

        if onbin:
            if gyou in ["ダ", "ナイ"]:
                katsuyou = target_katsuyou[form][1]
            else:
                katsuyou = target_katsuyou[form][0]

        elif not onbin:
            katsuyou = target_katsuyou[form][0]

    return katsuyou


if __name__ == '__main__':
    debug = True
    origin, type, form, onbin = [""]*4
    get_katsuyou(origin, type, form, onbin)
