str = "那时, 这里的山峰, 排列得跟棋盘上的棋子一般, 齐齐整整, 后来."
data_ch = set()
with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    for line in f:
        ch = line.split('=')[0]
        data_ch.add(ch)

positions = []
for index, character in enumerate(str):
    if character == ',' or character == '.':
        positions.append(index)

phrase_list = []
for p in range(0, len(positions)):
    y_list = []
    if p != 0:
        start = positions[p] - len(str[positions[p - 1]:positions[p]])
        end = positions[p]
        for x in range(start, end + 1):
            if y_list and x < y_list[-1]:
                continue
            elif y_list and x in positions:
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
            elif y_list and x in positions:
                phrase_list.append(str[x])
                continue
            for y in range(end, start, -1):
                if str[x:y] in data_ch:
                    phrase_list.append(str[x:y])
                    y_list.append(y)
                    break

print(phrase_list)