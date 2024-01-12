data_ch = set()
phrase_dict = {}

with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch, vi = line.strip().split('=')
        data_ch.add(ch)
        phrase_dict[ch] = vi.split('/')[0]

with open('test.txt', 'r', encoding='utf-8') as f:
    for line in f:
        positions = [index for index, character in enumerate(line) if character not in data_ch]

        phrase_list = []
        for p in range(len(positions)):
            y_list = []
            if p != 0:
                start = positions[p] - len(line[positions[p - 1]:positions[p]])
                end = positions[p]
                for x in range(start, end + 1):
                    if y_list and x < y_list[-1]:
                        continue
                    elif x == positions[p]:
                        phrase_list.append(line[x])
                        continue
                    for y in range(end, start, -1):
                        if line[x:y] in data_ch:
                            phrase_list.append(line[x:y])
                            y_list.append(y)
                            break
            elif p == 0:
                start = len(line[0:positions[0]]) - positions[0]
                end = len(line[0:positions[0]])
                for x in range(start, end + 1):
                    if y_list and x < y_list[-1]:
                        continue
                    elif x == positions[p]:
                        phrase_list.append(line[x])
                        continue
                    for y in range(end, start, -1):
                        if line[x:y] in data_ch:
                            phrase_list.append(line[x:y])
                            y_list.append(y)
                            break
        result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])
        result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])

        result = result.replace('，', ',')
        result = result.replace(' .', '.')
        result = result.replace(' ,', ',')
        result = result.replace('  ', ' ')
        result = result.replace(' !', '!')
        result = result.replace(' ?', '?')

        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(result + '\n')