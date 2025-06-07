import re

def capitalize_after_punctuation(string):
    pattern = r'(?<=[.!?":“\n])\s*(\w)'
    result = re.sub(pattern, lambda m: m.group(0).upper(), string)
    return result

data_ch = set()
phrase_dict = {}

with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch, vi = line.strip().split('=')
        data_ch.add(ch)
        phrase_dict[ch] = vi.split('/')[0]

with open('test.txt', 'r', encoding='utf-8') as f:
    content = ''
    for index, line in enumerate(f):
        positions = []
        characters = ['.', ',', '!', '?', ':', ';', '(', ')', '"', '“', '”', '\n', '=']
        for index, character in enumerate(line):  
            if character in characters:
                positions.append(index)
        if line[-1] not in characters:
            positions.append(len(line))
        phrase_list = []
        for p in range(len(positions)):
            y_list = []
            if p != 0:
                start = positions[p - 1] 
                end = positions[p]
                for x in range(start + 1, end + 1):
                    if x > line.index(line[-1]):
                        break
                    if line[x] == ' ':  
                        continue
                    elif y_list and x < y_list[-1]:
                        continue
                    elif x == positions[p]:
                        phrase_list.append(line[x])  
                        continue
                    for y in range(end, -1, -1):
                        if y_list and y < y_list[-1]:
                            break
                        elif line[x:y] in data_ch:  
                            phrase_list.append(line[x:y])  
                            y_list.append(y)
                            break
                        elif line[x] not in data_ch and line[y] not in data_ch :  
                            if x == y or x == y - 1:
                                phrase_list.append(line[x])  
                                y_list.append(y)
                                break
                            else:   
                                if len(line[x:y]) == 2:  
                                    phrase_list.append(line[x:y])  
                                    y_list.append(y)
                                    break
                                else:
                                    for index, i in enumerate(line[x+1:y]):  
                                        if i not in data_ch and index == len(line[x+1:y-1]) - 1:  
                                            phrase_list.append(line[x:y])  
                                            y_list.append(y)
                                            break
                                        elif i not in data_ch and index < len(line[x+1:y-1]) - 1:
                                            continue
                                        else:
                                            break
            elif p == 0:
                end = positions[p]
                for x in range(0, end + 1):
                    if x > line.index(line[-1]):
                        break
                    if line[x] == ' ':  
                        continue
                    elif y_list and x < y_list[-1]:
                        continue
                    elif x == positions[p]:
                        phrase_list.append(line[x])  
                        continue
                    for y in range(end, -1, -1):
                        if y_list and y < y_list[-1]:
                            break
                        elif line[x:y] in data_ch:  
                            phrase_list.append(line[x:y])  
                            y_list.append(y)
                            break
                        elif line[x] not in data_ch and line[y] not in data_ch :  
                            if x == y or x == y - 1:
                                phrase_list.append(line[x])  
                                y_list.append(y)
                                break
                            else:   
                                if len(line[x:y]) == 2:  
                                    phrase_list.append(line[x:y])  
                                    y_list.append(y)
                                    break
                                else:
                                    for index, i in enumerate(line[x+1:y]):  
                                        if i not in data_ch and index == len(line[x+1:y-1]) - 1:  
                                            phrase_list.append(line[x:y])  
                                            y_list.append(y)
                                            break
                                        elif i not in data_ch and index < len(line[x+1:y-1]) - 1:
                                            continue
                                        else:
                                            break
        result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])   
        result = result.replace('，', ', ')
        result = result.replace(' . ', '. ')
        result = result.replace(' , ', ', ')
        result = result.replace('  ', ' ')
        result = result.replace(' ! ', '! ')
        result = result.replace(' ? ', '? ')
        result = result.replace(' : ', ': ')
        result = result.replace(' ; ', '; ')
        result = result.replace(' ) ', ') ')
        result = result.replace('( ', '(')
        result = result.replace('“ ', '“')
        result = result.replace(' ”', '”')
        result = result.replace(' ‘', '‘')
        result = result.replace('’ ', '’')
        result = result.replace(' 、', ',')
        result = result.replace('.', '. ')
        result = result.replace(',', ', ')
        result = result.replace('：', ':')
        result = result.strip()
        result += '\n'
        
        content += capitalize_after_punctuation(result)
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(content)