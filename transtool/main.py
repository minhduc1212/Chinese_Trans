str = " 大奉京兆府，监牢. 牢. A."
str = str.replace('，', ',')
str = str.replace('。', '.')
data_ch = set()
phrase_dict = {}

with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch, vi = line.strip().split('=')
        data_ch.add(ch)
        phrase_dict[ch] = vi.split('/')[0]


#tìm các ký tự không phải tiếng trung
positions = [index for index, character in enumerate(str) if character not in data_ch]

phrase_list = []
for p in range(0, len(positions)):
    y_list = []
    if p != 0:
        start = positions[p] - len(str[positions[p - 1]:positions[p]])
        end = positions[p]
        for x in range(start, end + 1):
            if y_list and x < y_list[-1]:   
                continue
            elif x == positions[p]:
                phrase_list.append(str[x])
                continue
            for y in range(end, start, -1):
                if str[x:y] in data_ch:
                    phrase_list.append(str[x:y])
                    y_list.append(y)
                    break

    elif p == 0:
        start = len(str[0:positions[0]]) - positions[0]
        end = len(str[0:positions[0]])
        for x in range(start, end + 1):
            if y_list and x < y_list[-1]:
                continue
            elif x == positions[p]:
                phrase_list.append(str[x])
                continue
            for y in range(end, start, -1):
                if str[x:y] in data_ch:
                    phrase_list.append(str[x:y])
                    y_list.append(y)
                    break

result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])

result = result.replace('，', ',')
result = result.replace(' .', '.')
result = result.replace(' ,', ',')
result = result.replace('  ', ' ')
result = result.replace(' !', '!')
result = result.replace(' ?', '?')



print(result) 