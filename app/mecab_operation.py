import MeCab

# MeCab data → list of dictionary
def mecab_dict(text):
    tagger = MeCab.Tagger()
    tagger.parse('')
    tagger.parseToNode('dummy')
    node = tagger.parseToNode(text)
    word_class = []
    """
    word_class
    {   "word": 形態素,
        "part": 品詞,
        "subpart1": 品詞細分類1（普通名詞、格助詞、非自立可能など）,
        "subpart2": 品詞細分類2（一般など）,
        "type": 活用形（五段-ラ行、助動詞-タなど）,
        "form": 活用型（連用形-イ音便、終止形-一般など）,
        "origin": 原型 ,
        "kana": カナ    }
    """
    while node:
        word = node.surface
        wclass = node.feature.split(',')
        if wclass[0] != 'BOS/EOS':
            # 日本語のとき
            try:
                word_class.append({"word": word, "part": wclass[0], "subpart1": wclass[1], "subpart2": wclass[2], "type": wclass[4], "form": wclass[5], "origin": wclass[10], "kana": wclass[11]})
            # 英語のとき
            except:
                word_class.append({"word": word, "part": wclass[0], "subpart1": wclass[1], "subpart2": wclass[2], "type": wclass[4], "form": wclass[5], "origin": "", "kana": ""})
        node = node.next
    return word_class


class Keitaiso():

    def __init__(self, word_class):
        self.word_class = word_class
        self.LAST = len(word_class) - 1

    # Get details of keitaiso
    def keitaiso_detail(self, word_dict):
        return word_dict['word'], word_dict['part'], word_dict['type'], word_dict['form'].split('-')[0], word_dict['origin'], word_dict['kana']



    def get_now(self, now):
        return self.keitaiso_detail(self.word_class[now])


    def get_all(self, now):
        now_dict = self.word_class[now]
        if self.LAST == 0:
            return self.keitaiso_detail(now_dict) + \
                    ("", "", "", "", "", "") + \
                    ("", "", "", "", "", "")
        elif now == 0:
            return self.keitaiso_detail(now_dict) + \
                    ("", "", "", "", "", "") + \
                    self.keitaiso_detail(self.word_class[now+1])
        elif now == self.LAST:
            return self.keitaiso_detail(now_dict) + \
                    self.keitaiso_detail(self.word_class[now-1]) + \
                    ("", "", "", "", "", "")
        else:
            return self.keitaiso_detail(now_dict) + \
                    self.keitaiso_detail(self.word_class[now-1]) + \
                    self.keitaiso_detail(self.word_class[now+1])
