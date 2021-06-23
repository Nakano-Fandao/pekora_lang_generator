# -*- coding: utf-8 -*-

# Modules
from katsuyou import get_katsuyou
from mecab_operation import Keitaiso

# 丁寧御を除去
def remove_teinei(word_class):
    """
        p_word1:    previous keitaiso
        word0:      current keitaiso
        word1:      next keitaiso
    """

    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    sentence = ""

    for i, word_dict in enumerate(word_class):

        word0, part0, subpart0, form0, origin0, kana0 = keitaiso.get(i, word=True, part=True, subpart1=True, form=True, origin=True, kana=True)
        if i != 0:
            p_word1, p_part1, p_subpart1, p_type1, p_form1, p_origin1, p_kana1 = keitaiso.get(i-1, word=True, part=True, subpart1=True, type=True, form=True, origin=True, kana=True)
        else:
            sentence += word0
            continue
        if i != LAST:
            part1, origin1, kana1 = keitaiso.get(i+1, part=True, origin=True, kana=True)

        if i != 0:
            if (p_part1 == '補助記号') & (p_word1 not in ["。", "、"]):
                sentence += word0
                continue

        if part0 == "接頭辞":
            o_escape_list = ["ハシ", "メデタイ", "ミソシル", "コメ", "ウチ", "セワ"]
            go_escape_list = ["ハン"]
            if ((kana0 in ["オ"]) & (kana1 not in o_escape_list)) | \
                ((kana0 in ["ゴ"]) & (kana1 not in go_escape_list)):
                continue

        elif part0 == '助動詞':

            # 「た」に繋がるため音便あり
            onbin = (False, True) [kana1 in ['タ']]

            if origin0 == 'ます':

                if p_origin1 in ["ござる", "御座る"]:

                    if word_class[i-2]["part"] == '助動詞':

                        # で-ござい-ます-△ → だ-△
                        sentence = sentence.rsplit(p_word1, 1)[0][:-1] + get_katsuyou("", "助動詞-ダ", form0, onbin)
                        continue

                    # おはようございます、など
                    else:
                        # 〇-ござい-ます-△ → 〇-△
                        sentence = sentence.rsplit(p_word1, 1)[0]
                        continue

                elif p_origin1 in ["いたす", "致す"]:
                    # いたし-ます-△ → する-△
                    sentence = sentence.rsplit(p_word1, 1)[0] + get_katsuyou("する", "サ行変格", form0, onbin)
                    continue

                elif (p_origin1 in ["おる"]):
                    if (word_class[i-2]["origin"] == "を") | (i<=2):
                        sentence = sentence.rsplit(p_word1, 1)[0] + get_katsuyou("おる", "五段-ラ行", form0, onbin)
                        continue
                    else:
                        # て-おり-ます-△ → て-いる-△
                        sentence = sentence.rsplit(p_word1, 1)[0] + get_katsuyou("いる", "上一段-ア行", form0, onbin)
                        continue

                elif (p_origin1 in ["居る"]):
                    sentence = sentence.rsplit(p_word1, 1)[0] + get_katsuyou("いる", "上一段-ア行", form0, onbin)
                    continue

                elif (p_kana1 == "アル") & (kana1 in ["ナイ", "ヌ"]):
                    sentence = sentence.rsplit(p_word1, 1)[0]
                    continue

                else:
                    sentence = sentence.rsplit(p_word1, 1)[0] + get_katsuyou(p_origin1, p_type1, form0, onbin)
                    continue

            elif origin0 == 'です':
                if (origin1 in ["か"]) & (part1 == "助詞"):
                    if (p_origin1 == "ん") & (p_part1 == '助詞'):
                        sentence = sentence[:-1]
                elif p_kana1 in ["ホシー"]:
                    pass
                else:
                    # 助動詞「ダ」で、１つ後の形態素に合うものを取得し追加
                    sentence += get_katsuyou("", "助動詞-ダ", form0, onbin)
                continue

            elif origin0 == "ぬ":
                if p_form1 == "未然形":
                    sentence += get_katsuyou("", "助動詞-ナイ", form0, onbin)
                    continue

        elif subpart0 == '終助詞':

            if p_subpart1 == "終助詞":
                continue

        sentence += word0

    return sentence

if __name__ == '__main__':
    debug = True
    remove_teinei("word_class")
