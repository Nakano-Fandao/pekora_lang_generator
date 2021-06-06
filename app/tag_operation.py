import re

def replace_tags(sentence):

    # Create pattern list
    tag_list = [
        '<a.*?>',
        "</a>",
        '<button.*?>',
        "</button>",
        '<cite.*?>',
        "</cite>",
        '<code.*?>',
        "</code>",
        '<iframe.*?>',
        "</iframe>",
        '<img.*?>',
        "</img>",
        '<input.*?>',
        "</input>",
        '<label.*?>',
        "</label>",
        '<select.*?>',
        "</select>",
        '<span.*?>',
        "</span>",
        '<strong.*?>',
        "</strong>",
    ]

    # Tag pattern
    patterns = re.compile(('|').join(tag_list))

    # Matched tags
    tags = patterns.findall(sentence)

    # Replacing process
    replaced_sentence = re.sub(('|').join(tags), "TAG_FLAG", sentence)

    return replaced_sentence, tags

def return_tags(sentence, tags):

    for tag in tags:
        sentence = sentence.replace("TAG_FLAG", tag, 1)

    return sentence


sentence = """
"""

if __name__ == "__main__":
    replace_tags(sentence)
