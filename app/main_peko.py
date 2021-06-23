# -*- coding: utf-8 -*-

# Modules
from icecream import ic
from sonkei_kenjou import remove_sonken
from teinei import remove_teinei
from mecab_operation import mecab_dict
from peko_nai import exchange_pekonai
from not_used_convert_natural import convert_natural_to_peko
from insert_peko import add_peko
from pekora_phrasing import introduce_pekora_phrasing
from tag_operation import replace_tags, return_tags

# Mode
debug = False
production = False

def peko_main(sentence):

    # エラー無視の関数
    if production: return no_stop(sentence)

    # エラーで止まる通常の関数
    else: return normal(sentence)

sentence = """サンプルです。
"""

def normal(sentence):

    # Replace_tags with "TAG_FLAG"
    no_tag_sentence, tags = replace_tags(sentence)

    # 尊敬語・謙譲語を除去
    word_class = mecab_dict(no_tag_sentence)
    no_sonken_sentence = remove_sonken(word_class)

    # 丁寧語を除去
    no_sonken_word_class = mecab_dict(no_sonken_sentence)
    natural_sentence = remove_teinei(no_sonken_word_class)

    # ないの？　→　ねぇーの？
    pekonai = exchange_pekonai(natural_sentence)

    # 文中・文末にぺこを入れる
    peko_inserted = add_peko(pekonai)

    # 特定のぺこらの言い回しを入れる
    peko_sentence = introduce_pekora_phrasing(peko_inserted)

    # Placed back tags to the original positions
    perfect_peko_sentence = return_tags(peko_sentence, tags) if tags else peko_sentence

    if debug:
        ic(no_tag_sentence)
        ic(no_sonken_sentence)
        ic(natural_sentence)
        ic(pekonai)
        ic(peko_inserted)
        ic(peko_sentence)
        ic(perfect_peko_sentence)

    return perfect_peko_sentence


def no_stop(sentence):

    error_count = 0

    # Replace_tags with "TAG_FLAG"
    try:
        no_tag_sentence, tags = replace_tags(sentence)
    except Exception as e:
        print(e)
        error_count += 1
        no_tag_sentence = sentence
    except:
        error_count += 1
        no_tag_sentence = sentence

    # 尊敬語・謙譲語を除去
    try:
        word_class = mecab_dict(no_tag_sentence)
        no_sonken_sentence = remove_sonken(word_class)
    except Exception as e:
        print(e)
        error_count += 1
        no_sonken_sentence = no_tag_sentence
    except:
        error_count += 1
        no_sonken_sentence = no_tag_sentence

    # 丁寧語を除去
    try:
        no_sonken_word_class = mecab_dict(no_sonken_sentence)
        natural_sentence = remove_teinei(no_sonken_word_class)
    except Exception as e:
        print(e)
        error_count += 1
        natural_sentence = no_sonken_sentence
    except:
        error_count += 1
        natural_sentence = no_sonken_sentence

    # 常体をぺこら語に変換
    # natural_word_class = mecab_dict(natural_sentence)
    # peko_sentence = convert_natural_to_peko(natural_word_class)
    # print(peko_sentence)

    # ないの？　→　ねぇーの？
    try:
        pekonai = exchange_pekonai(natural_sentence)
    except Exception as e:
        print(e)
        error_count += 1
        pekonai = natural_sentence
    except:
        error_count += 1
        pekonai = natural_sentence

    # 文中・文末にぺこを入れる
    try:
        peko_inserted = add_peko(pekonai)
    except Exception as e:
        print(e)
        error_count += 1
        peko_inserted = pekonai
    except:
        error_count += 1
        peko_inserted = pekonai

    # 特定のぺこらの言い回しを入れる
    try:
        peko_sentence = introduce_pekora_phrasing(peko_inserted)
    except Exception as e:
        print(e)
        error_count += 1
        peko_sentence = peko_inserted
    except:
        error_count += 1
        peko_sentence = peko_inserted

    # Placed back tags to the original positions
    try:
        perfect_peko_sentence = return_tags(peko_sentence, tags) if tags else peko_sentence
    except Exception as e:
        print(e)
        error_count += 1
        perfect_peko_sentence = peko_sentence
    except:
        error_count += 1
        perfect_peko_sentence = peko_sentence

    print(f"{error_count} error occurred")

    return perfect_peko_sentence


if __name__ == '__main__':
    debug = True
    production = False
    peko_main(sentence)
