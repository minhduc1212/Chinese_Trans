import re

def capitalize_after_punctuation(string):
    return string.capitalize() # Đơn giản capitalize() toàn bộ chuỗi đầu ra

str_input = '心目中神豪第一文' # Đổi tên biến để rõ ràng hơn
data_ch = set()
phrase_dict = {}

with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch, vi = line.strip().split('=')
        data_ch.add(ch)
        phrase_dict[ch] = vi.split('/')[0]

phrase_list = []
i = 0
n = len(str_input) # Sử dụng str_input thay vì str
while i < n:
    found_phrase = False
    for j in range(n, i, -1):
        phrase = str_input[i:j] # Sử dụng str_input thay vì str
        if phrase in data_ch:
            phrase_list.append(phrase)
            i = j
            found_phrase = True
            break
    if not found_phrase:
        phrase_list.append(str_input[i]) # Sử dụng str_input thay vì str
        i += 1

print(phrase_list)
result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])

result = re.sub(r'[，. ]+', lambda m: m.group(0).replace('，', ',').replace(' .', '.').replace(' ,', ',').replace('  ', ' '), result)
result = re.sub(r' [!?]', lambda m: m.group(0).replace(' !', '!').replace(' ?', '?'), result)

print(capitalize_after_punctuation(result)) # Gọi capitalize_after_punctuation với kết quả đã dịch