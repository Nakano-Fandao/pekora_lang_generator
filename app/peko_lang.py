import MeCab
import json

# Constants
noun = '名詞'
verb = '動詞'
adjective = '形容詞'
pronoun = '代名詞'
adverb = '副詞'
preposition = '前置詞'
conjunction = '接続詞'
interjection ='間投詞'

json_path = './json_folder/katsuyou.json'
with open(json_path) as f:
    katsuyou_json = json.load(f)


# 敬体を常体に変換
def convert_distal_to_natural(word_class):

    sentence = ""

    for i, word_dict in enumerate(word_class):

        # 現在と前後の形態素の詳細を取得
        word, part, type, form, origin = get_keitaiso_detail(word_dict)
        if i != 0:
            pre_word_dict = word_class[i-1]
            pre_word, pre_part, pre_type, pre_form, pre_origin = get_keitaiso_detail(pre_word_dict)
        if i != len(word_class)-1:
            post_word, post_part, post_type, post_form, post_origin = get_keitaiso_detail(word_class[i+1])


        print(word, part, type, form, origin)


        if part == '助動詞':

            # 連用形のとき、「た」に繋がるため音便あり
            onbin = (False, True) [form in ['連用形']]

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

                else:
                    sentence = sentence.rsplit(pre_word, 1)[0] + get_katsuyou(pre_origin, pre_type, form, onbin)
                    continue

            if origin == 'です':
                if (post_origin in ["か"]) & (post_part == "助詞"):
                    continue
                else:
                    # 助動詞「ダ」で、１つ後の形態素に合うものを取得し追加
                    sentence += get_katsuyou("", "助動詞-ダ", form, onbin)
                    continue

        elif word_dict['subpart1'] == '終助詞':

            if pre_word_dict['subpart1'] == "終助詞":
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

    # 動詞-変格活用 以外のとき
    if '-' in type: # type = "五段活用-ア行" or "助動詞-ダ"
        dan, gyou = type.split('-')
        target_katsuyou = katsuyou_json[dan][gyou]

    # 動詞-変格活用のとき
    else: # type = "カ行変格"
        dan = type
        target_katsuyou = katsuyou_json[dan]

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
            if gyou in ["ダ"]:
                katsuyou = target_katsuyou[form][1]

        elif not onbin:
            katsuyou = target_katsuyou[form][0]

    return katsuyou

# 形態素の詳細を取得する関数
def get_keitaiso_detail(word_dict):
    return word_dict['word'], word_dict['part'], word_dict['type'], word_dict['form'].split('-')[0], word_dict['origin']

def mecab_dict(text):
    tagger = MeCab.Tagger()
    tagger.parse('')
    node = tagger.parseToNode(text)
    word_class = []
    """
    word_class
    {   "word": 形態素,
        "part": 品詞,
        "subpart1": 品詞細分類1（普通名詞、格助詞、非自立可能など）,
        "subpart2": 品詞細分類2（一般など）,
        "subpart3": 品詞細分類3（）,
        "type": 活用形（五段-ラ行、助動詞-タなど）,
        "form": 活用型（連用形-イ音便、終止形-一般など）,
        "origin": 原型    }
    """
    while node:
        word = node.surface
        wclass = node.feature.split(',')
        if wclass[0] != 'BOS/EOS':
            # 日本語のとき
            try:
                word_class.append({"word": word, "part": wclass[0], "subpart1": wclass[1], "subpart2": wclass[2], "subpart3": wclass[3], "type": wclass[4], "form": wclass[5], "origin": wclass[10]})
            # 英語のとき
            except:
                word_class.append({"word": word, "part": wclass[0], "subpart1": wclass[1], "subpart2": wclass[2], "subpart3": wclass[3], "type": wclass[4], "form": wclass[5], "origin": ""})
        node = node.next
    return word_class

def convert_natural_to_peko(word_class):
    sentence = ""

    for i, word_dict in enumerate(word_class):

        # 現在と前後の形態素の詳細を取得
        word, part, type, form, origin = get_keitaiso_detail(word_dict)

        if form == '終止形':
            sentence += word + "ぺこ"
            continue

        elif (word in ['か', 'の']) & (word_dict['subpart1'] == "終助詞"):
            sentence += "ぺこ"
            continue

        sentence += word

    return sentence

def main(sentence_list):
    natural_sentence_list = []
    for sentence in sentence_list:
        word_class = mecab_dict(sentence)
        natural_sentence_list.append(convert_distal_to_natural(word_class))

    peko_sentence_list = []
    for natural_sentence in natural_sentence_list:
        natural_word_class = mecab_dict(natural_sentence)
        peko_sentence_list.append(convert_natural_to_peko(natural_word_class))

    print(peko_sentence_list)

    return peko_sentence_list


sentence = ["[「」]", ""]

main(sentence)
