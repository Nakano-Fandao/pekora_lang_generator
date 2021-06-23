# -*- coding: utf-8 -*-

# Modules
import re
from icecream import ic

# Mode
debug = False

def replace_tags(sentence):

    # Create pattern list
    tag_list = ['a', 'button', 'cite', 'code', 'iframe', 'img', 'input', 'label', 'select', 'span', 'strong', 'ruby', 'rt']

    pattern_list = \
        [f'<{tag}.*?>' for tag in tag_list] + \
        [f"</{tag}>" for tag in tag_list]

    # Tag pattern
    patterns = re.compile(('|').join(pattern_list))

    # Matched tags
    tags = patterns.findall(sentence)

    if not tags:
        if debug: ic(sentence, tags)
        return sentence, tags

    # Replacing process
    replaced_sentence = re.sub(re.compile(('|').join(tags)), "TAG_FLAG", sentence)

    if debug: ic(replaced_sentence, tags)
    return replaced_sentence, tags


def return_tags(sentence, tags):

    for tag in tags:
        sentence = sentence.replace("TAG_FLAG", tag, 1)

    return sentence


sentence = """な<a href="javascript:void(0)" class="dicWin" id="id-0002"><span class="under">ミス</span></a>・<a href="javascript:void(0)" class="dicWin" id="id-0003"><span class="under">コンテスト</span></a>に、<ruby>大学生<rt>だいがくせい</rt>
"""

if __name__ == "__main__":
    debug = True
    replace_tags(sentence)
