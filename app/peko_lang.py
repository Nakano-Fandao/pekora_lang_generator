import json

from mecab_operation import mecab_dict, Keitaiso

# Constants
json_path = './json_folder/'
with open(json_path+"katsuyou.json") as f:
    katsuyou_json = json.load(f)
with open(json_path+"sonkei_kenjou.json") as f:
    sonken_json = json.load(f)

# 尊敬語・謙譲語を除去
def remove_sonken(word_class):

    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    sentence = ""
    action_word = ""
    katsuyou_flag = False
    skip_flag = False

    for i, word_dict in enumerate(word_class):

        word, part, type, form, origin, kana, \
        pre_word, pre_part, pre_type, pre_form, pre_origin, pre_kana, \
        post_word, post_part, post_type, post_form, post_origin, post_kana \
            = keitaiso.get_all(i)

        if skip_flag:
            if kana == action_word:
                # 連用形のとき、「た」に繋がるため音便あり
                onbin = (False, True) [post_kana in ['タ']]
                sentence += get_katsuyou(natural_origin, natural_type, form, onbin)
                skip_flag = False

            continue

        elif katsuyou_flag:
            sentence += get_katsuyou(natural_origin, natural_type, katsuyou_flag, False)
            katsuyou_flag = False

        elif (part == "接頭辞") & (kana in ["オ", "ゴ"]):

            if post_part == "動詞":
                if post_kana in list(sonken_json):
                    natural_origin = sonken_json[post_kana]['常体']
                    natural_type = sonken_json[post_kana]["段-行"]

                # "お買いになる"などセットで尊敬・謙譲語になるもの
                else:
                    natural_origin = post_origin
                    natural_type = post_type

                if i == LAST-1:
                    katsuyou_flag = "命令形"
                    continue

                elif i < LAST-1:
                    skip_flag = True
                    if word_class[i+2]['kana'] in ["クダサル", "イタス"]:
                        action_word = word_class[i+2]['kana']

                    elif word_class[i+2]['kana'] != 'ニ':
                        skip_flag = False
                        katsuyou_flag = "命令形"

                    elif i < LAST-2:
                        if (word_class[i+2]['kana'] == "ニ") & (word_class[i+3]['kana'] == "ナル"):
                            action_word = "ナル"

                continue

            elif post_part == "名詞":

                if post_kana in ["カケ", "メシ", "ラン"]:
                    natural_origin = sonken_json[post_kana]['常体']
                    natural_type = sonken_json[post_kana]['段-行']
                    skip_flag = True

                    if (word_class[i+2]['kana'] == "ニ") & (word_class[i+3]['kana'] == "ナル"):
                        action_word = "ナル"

                    elif word_class[i+2]['kana'] == "クダサル":
                        action_word = "クダサル"

                    else:
                        action_word = post_word

                    continue

        elif (part == "名詞") & (kana in ["ゴラン"]):
                    natural_origin = sonken_json[kana[1:]]['常体']
                    natural_type = sonken_json[kana[1:]]['段-行']
                    skip_flag = True

                    if i == LAST:
                        sentence += get_katsuyou(natural_origin, natural_type, "命令形", False)

                    elif post_kana == "クダサル":
                        action_word = "クダサル"

                    elif i < LAST-1:
                        if (post_kana == "ニ") & (word_class[i+2]['kana'] == "ナル"):
                            action_word = "ナル"

                    else:
                        skip_flag = False
                        sentence += get_katsuyou(natural_origin, natural_type, "命令形", False)

                    continue

        elif part == "動詞":

            # 連用形のとき、「た」に繋がるため音便あり
            onbin = (False, True) [post_kana in ['タ']]

            sonken_list = list(sonken_json)
            if kana in sonken_list:
                if post_kana in ["アゲル"]:
                    natural_origin = sonken_json[kana+post_kana]['常体']
                    natural_type = sonken_json[kana+post_kana]['段-行']
                    skip_flag = True
                    action_word = 'アゲル'
                else:
                    sentence += get_katsuyou(sonken_json[kana]['常体'], sonken_json[kana]['段-行'], form, onbin)
                    continue

        elif part == "助動詞":

            # 連用形のとき、「た」に繋がるため音便あり
            onbin = (False, True) [post_kana in ['タ']]

            if kana in ["テラッシャル"]:
                original_json = sonken_json[kana]
                sentence += get_katsuyou(original_json['常体'], original_json['段-行'], form, onbin)
                continue

        sentence += word

    return sentence

# 丁寧御を除去
def remove_teinei(word_class):

    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)

    sentence = ""

    for i, word_dict in enumerate(word_class):

        word, part, type, form, origin, kana, \
        pre_word, pre_part, pre_type, pre_form, pre_origin, pre_kana, \
        post_word, post_part, post_type, post_form, post_origin, post_kana \
            = keitaiso.get_all(i)

        if i != 0:
            if (pre_part == '補助記号') & (pre_word not in ["。", "、"]):
                sentence += word
                continue

        if part == "接頭辞":
            o_escape_list = ["ハシ", "メデタイ", "ミソシル", "コメ", "ウチ", "セワ"]
            go_escape_list = ["ハン"]
            if ((kana in ["オ"]) & (post_kana not in o_escape_list)) | \
                ((kana in ["ゴ"]) & (post_kana not in go_escape_list)):
                continue

        elif part == '助動詞':

            # 連用形のとき、「た」に繋がるため音便あり
            onbin = (False, True) [post_kana in ['タ']]

            if origin == 'ます':

                if pre_origin in ["ござる", "御座る"]:

                    if word_class[i-2]["part"] == '助動詞':

                        # で-ござい-ます-△ → だ-△
                        sentence = sentence.rsplit(pre_word, 1)[0][:-1] + get_katsuyou("", "助動詞-ダ", form, onbin)
                        continue

                    # おはようございます、など
                    else:
                        # 〇-ござい-ます-△ → 〇-△
                        sentence = sentence.rsplit(pre_word, 1)[0]
                        continue

                elif pre_origin in ["いたす", "致す"]:
                    # いたし-ます-△ → する-△
                    sentence = sentence.rsplit(pre_word, 1)[0] + get_katsuyou("する", "サ行変格", form, onbin)
                    continue

                elif (pre_origin in ["おる"]):
                    if (word_class[i-2]["origin"] == "を") | (i<=2):
                        sentence = sentence.rsplit(pre_word, 1)[0] + get_katsuyou("おる", "五段-ラ行", form, onbin)
                        continue
                    else:
                        # て-おり-ます-△ → て-いる-△
                        sentence = sentence.rsplit(pre_word, 1)[0] + get_katsuyou("いる", "上一段-ア行", form, onbin)
                        continue

                elif (pre_origin in ["居る"]):
                    sentence = sentence.rsplit(pre_word, 1)[0] + get_katsuyou("いる", "上一段-ア行", form, onbin)
                    continue

                else:
                    sentence = sentence.rsplit(pre_word, 1)[0] + get_katsuyou(pre_origin, pre_type, form, onbin)
                    continue

            elif origin == 'です':
                if (post_origin in ["か"]) & (post_part == "助詞"):
                    if (pre_origin == "ん") & (pre_part == '助詞'):
                        sentence = sentence[:-1]
                    continue
                else:
                    # 助動詞「ダ」で、１つ後の形態素に合うものを取得し追加
                    sentence += get_katsuyou("", "助動詞-ダ", form, onbin)
                    continue

            elif origin == "ぬ":
                if pre_form == "未然形":
                    sentence += get_katsuyou("", "助動詞-ナイ", form, onbin)
                    continue

        elif word_dict['subpart1'] == '終助詞':

            if word_class[i-1]['subpart1'] == "終助詞":
                continue

        sentence += word

    return sentence

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

    # katsuyou = ''

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

        elif not onbin:
            katsuyou = target_katsuyou[form][0]

    return katsuyou

def convert_natural_to_peko(word_class):

    def normal_peko_translate(word):
        if word in ["だ"]:
            add_word = "ぺこ"
        else:
            add_word = word + "ぺこ"
        return add_word

    LAST = len(word_class)-1
    keitaiso = Keitaiso(word_class)
    sentence = ""

    for i, word_dict in enumerate(word_class):

        word, part, type, form, origin, kana = keitaiso.get_now(i)

        if form in ['終止形', "命令形"]:
            if i != LAST:
                if word_class[i+1]['word'] in ["か", "の"]:
                    sentence += word
                elif word_class[i+1]['part'] in ["助動詞"]:
                    sentence += word
                else:
                    sentence += normal_peko_translate(word)
            else:
                sentence += normal_peko_translate(word)
            continue

        elif (form in ["連体形"]) & (i != LAST):
            if word_class[i+1]['word'] == "<":
                sentence += normal_peko_translate(word)
                continue

        elif (word in ['か', 'の']) & (word_dict['subpart1'] == "終助詞"):
            sentence += "ぺこ"
            continue

        sentence += word

    return sentence

def peko_main(sentence):

    # 尊敬語・謙譲語を除去
    word_class = mecab_dict(sentence)
    no_sonken_sentence = remove_sonken(word_class)
    print(no_sonken_sentence)

    # 丁寧語を除去
    no_sonken_word_class = mecab_dict(no_sonken_sentence)
    natural_sentence = remove_teinei(no_sonken_word_class)
    print(natural_sentence)

    # 常体をぺこら語に変換
    natural_word_class = mecab_dict(natural_sentence)
    peko_sentence = convert_natural_to_peko(natural_word_class)
    print(peko_sentence)

    return peko_sentence

sentence = """
"""

if __name__ == '__main__':
    peko_main(sentence)
