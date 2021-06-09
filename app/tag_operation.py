import re

def replace_tags(sentence):

    # Create pattern list
    tag_list = ['a', 'button', 'cite', 'code', 'iframe', 'img', 'input', 'label', 'select', 'span', 'strong']

    pattern_list = \
        [f'<{tag}.*?>' for tag in tag_list] + \
        [f"</{tag}>" for tag in tag_list]

    # Tag pattern
    patterns = re.compile(('|').join(pattern_list))

    # Matched tags
    tags = patterns.findall(sentence)

    if not tags:
        return sentence, tags

    # Replacing process
    replaced_sentence = re.sub(('|').join(tags), "TAG_FLAG", sentence)

    print(replaced_sentence)

    return replaced_sentence, tags


def return_tags(sentence, tags):

    for tag in tags:
        sentence = sentence.replace("TAG_FLAG", tag, 1)

    return sentence


sentence = """import文では、読み込むオブジェクト名と、モジュールファイルへのパスを指定します。この例では、module.jsファイルから関数helloをインポートしてます。オブジェクト名は「{}」で囲む必要があることに注意してください。
"""

if __name__ == "__main__":
    replace_tags(sentence)
