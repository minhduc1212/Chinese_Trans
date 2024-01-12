list = ['那时', ',', '这里', '的', '山峰', ',', '排列', '得', '跟', '棋盘上', '的', '棋子', '一般', ',', '齐齐整整', ',', '后来', '.']
with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    data_lines = f.readlines()

phrase_dict = {}
for data in data_lines:
    data = data.strip().split('=')
    ch = data[0]
    vi = data[1].split('/')[0]
    phrase_dict[ch] = vi

result = ' '.join([phrase_dict.get(phrase, phrase) for phrase in list])
print(result)