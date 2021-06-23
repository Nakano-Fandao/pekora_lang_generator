# -*- coding: utf-8 -*-

# Modules
import re
from icecream import ic

# Mode
debug = True

def replace_tags(sentence):

    # Create pattern list
    tag_list = ['a', 'button', 'cite', 'code', 'iframe', 'img', 'input', 'label', 'select', 'span', 'strong', 'ruby', 'rt']

    pattern_list = \
        [f'<{tag}[^>]*>' for tag in tag_list] + \
        [f"</{tag}>" for tag in tag_list]

    # Tag pattern
    patterns = re.compile(('|').join(pattern_list))

    # Matched tags
    tags = patterns.findall(sentence)

    if not tags:
        if debug: ic(sentence, tags)
        return sentence, tags

    # Replacing process
    replaced_sentence = re.sub(('|').join(tags), "TAG_FLAG", sentence)

    if debug: ic(replaced_sentence, tags)
    return replaced_sentence, tags


def return_tags(sentence, tags):

    for tag in tags:
        sentence = sentence.replace("TAG_FLAG", tag, 1)

    return sentence


sentence = """<li>
          <a href="https://nobunaga.hatenablog.jp/archive/category/c%2B%2B" class="category-c">
            c++ (16)
          </a>
          <a></a>
        </li>
"""

if __name__ == "__main__":
    debug = True
    sentence, tag = replace_tags(sentence)
    print(return_tags(sentence, tag))
