import re

def capitalize_after_punctuation(string):
    pattern = r'(?<=[.!?":“\n])\s*(\w)'
    result = re.sub(pattern, lambda m: m.group(0).upper(), string)
    return result

def remove_blank(txt):
  while True:
    if re.findall(r'(\d)\s+(\d)', txt):
      txt = re.sub(r'(\d)\s+(\d)', r'\1\2', txt)
    else:
        break
  return txt

with open('result.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text1 = text.replace('  ', ' ')
text1 = text1.replace(' ,', ',')

modified_text = capitalize_after_punctuation(text1)
modified_text = remove_blank(modified_text)
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(modified_text)