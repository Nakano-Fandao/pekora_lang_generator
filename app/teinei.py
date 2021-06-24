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

# 丁寧御を除去
def remove_teinei(sentence):
    """
        p_word1:    previous keitaiso
        word0:      current keitaiso
        word1:      next keitaiso
    """
    word_class = mecab_dict(sentence)
    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    s_list = []
    normal_skip = 0
    action_kana = ""
    n_origin = ""
    n_type = ""
    special_skip = False

    # 関数
    add = s_list.append
    pop = s_list.pop

    if debug: ic(word_class)

    for i in range(LAST+1):

        # skip処理
        if normal_skip > 0: normal_skip-= 1; continue

        #* 形態素情報を格納-----------------------------------------
        word0, part0, subpart0, type0, form0, origin0, kana0 = keitaiso.get(i, word=True, part=True, subpart1=True, type=True, form=True, origin=True, kana=True)
        if i > 0:
            p_word1, p_part1, p_subpart1, p_type1, p_form1, p_origin1, p_kana1 = keitaiso.get(i-1, word=True, part=True, subpart1=True, type=True, form=True, origin=True, kana=True)
            if i > 1:
                p_word2, p_part2, p_origin2 = keitaiso.get(i-2, word=True, part=True, origin=True)
            else:
                p_word2, p_part2, p_origin2 = [None]*3
        else:
            p_word1, p_part1, p_subpart1, p_type1, p_form1, p_origin1, p_kana1 = [None]*7
        if i < LAST:
            word1, part1, type1, origin1, kana1 = keitaiso.get(i+1, word=True, part=True, type=True, origin=True, kana=True)
            if i < LAST-1:
                form2, kana2 = keitaiso.get(i+2, form=True, kana=True)
            else:
                kana2 = None
        else:
            word1, part1, type1, origin1, kana1 = [None]*5

        if debug: ic(word0, part0, subpart0, form0, origin0, kana0)
        #* --------------------------------------------------------

        # Special skip
        if special_skip:
            if kana0 == action_kana:
                # 「た」に繋がるため音便あり
                onbin = (False, True) [kana1 in ['タ']]
                ic(n_origin, n_type, form0, onbin)
                ic(get_katsuyou(n_origin, n_type, form0, onbin))
                add(get_katsuyou(n_origin, n_type, form0, onbin))
                special_skip = False
            continue

        #* Main----------------------------------------------------
        if (p_part1 == '補助記号') & (p_word1 not in ["。", "、"]):
            add(word0)
            continue

        if part0 == "接頭辞":
            o_escape = set(["ハシ", "メデタイ", "ミソシル", "コメ", "ウチ", "セワ", "コエガケ"])
            go_escape = set(["ハン"])
            if ((kana0 in ["オ"]) & (kana1 not in o_escape)) | \
                ((kana0 in ["ゴ"]) & (kana1 not in go_escape)):
                continue

            elif kana2 == "クダサル":
                if form2 == "命令形":
                    add(word0)
                    add(word1)
                    add("ちょうだい")
                    normal_skip = 3
                else:
                    n_word = polite_json[kana1]
                    add(n_word["追加"])
                    n_origin = n_word['常体']
                    n_type = n_word["段-行"]
                    action_kana = kana2
                    special_skip = True
                continue

        elif part0 == '助動詞':

            # 「た」に繋がるため音便あり
            onbin = (False, True) [kana1 in ['タ']]

            if origin0 == 'ます':

                if p_origin1 in set(["ござる", "御座る"]):

                    # で-ござい-ます-△ → だ-△
                    if p_part2 == '助動詞':
                        pop(-1) # remove ござい
                        pop(-1) # remove で
                        add(get_katsuyou("", "助動詞-ダ", form0, onbin))
                        continue

                    # がございます、などございます → がある
                    elif p_word2 in set(["が", "など"]):
                        pop(-1) # remove ござい
                        pop(-1) # remove が or など
                        add("が")
                        add(get_katsuyou("ある", "五段-ラ行", form0, onbin))
                        continue

                    # おはようございます、など
                    else:
                        # 〇-ござい-ます-△ → 〇-△
                        pop(-1)
                        continue

                elif p_origin1 in ["いたす", "致す"]:
                    # いたし-ます-△ → する-△
                    pop(-1)
                    add(get_katsuyou("する", "サ行変格", form0, onbin))
                    continue

                elif (p_origin1 in ["おる"]):
                    if p_origin2 == "を":
                        pop(-1)
                        add(get_katsuyou("おる", "五段-ラ行", form0, onbin))
                        continue
                    else:
                        # て-おり-ます-△ → て-いる-△
                        pop(-1)
                        add(get_katsuyou("いる", "上一段-ア行", form0, onbin))
                        continue

                elif (p_origin1 in ["居る"]):
                    pop(-1)
                    add(get_katsuyou("いる", "上一段-ア行", form0, onbin))
                    continue

                elif (p_kana1 == "アル") & (kana1 in ["ナイ", "ヌ"]):
                    pop(-1)
                    continue

                else:
                    pop(-1)
                    add(get_katsuyou(p_origin1, p_type1, form0, onbin))
                    continue

            elif origin0 == 'です':
                if (origin1 in ["か"]) & (part1 == "助詞"):
                    if (p_origin1 == "ん") & (p_part1 == '助詞'):
                        pop(-1)
                elif p_kana1 in ["ホシー"]:
                    pass
                else:
                    # 助動詞「ダ」で、１つ後の形態素に合うものを取得し追加
                    add(get_katsuyou("", "助動詞-ダ", form0, onbin))
                continue

            elif origin0 == "ぬ":
                if p_form1 == "未然形":
                    add(get_katsuyou("", "助動詞-ナイ", form0, onbin))
                    continue

        elif subpart0 == '終助詞':

            if p_subpart1 == "終助詞":
                continue

        add(word0)

    return ''.join(s_list)

if __name__ == '__main__':
    sentence = """スタッフまでお声がけ下さったら、嬉しい。
    """
    debug = True
    remove_teinei(sentence)
