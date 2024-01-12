str = '这里'
with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    data_lines = f.readlines()
for data in data_lines:
    data = data.split('=')
    vi = data[1].split('/')
    ch = data[0]
    if ch == str:
        print(vi[0])
        break