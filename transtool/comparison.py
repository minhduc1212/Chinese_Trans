string = "那时, 这里的山峰, 排列得跟棋盘上的棋子一般, 齐齐整整, 后来."    

substrings_2 = []
substrings_1 = []
with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
    data_lines = f.readlines()
for data in data_lines:
    data = data.split('=')
    ch = data[0]
    if len(ch) == 2:
        substrings_2.append(ch)
    elif len(ch) == 1:
        substrings_1.append(ch)
with open('2.txt', 'w', encoding='utf-8') as f:
    f.write(str(substrings_2))
subtrings_in_string = []

string = string.replace(",", ",/")
string = string.replace(".", "./")
                    
for substring_2 in substrings_2:
    if substring_2 in string:
        subtrings_in_string.append(substring_2)
        string = string.replace(substring_2, f'{substring_2}/')
for substring_1 in substrings_1:
    positions = []
    characters = []
    for index, character in enumerate(string):
        if character == substring_1:
            positions.append(index)
            characters.append(character)
    for position in positions:
        if any (string[position:position+2] == substring_in_string for substring_in_string in subtrings_in_string) or any (string[position-2:position+1] == substring_in_string for substring_in_string in subtrings_in_string):
            continue
        else:
            string = string[:position+1] + "/" + string[position+1:]

string = string.replace("//", "/")
print(string)
string = string.split("/")
#loại bỏ các phần tử rỗng
string = [x for x in string if x]
#loại bỏ các khoảng trống trong phần tử
string = [x.strip() for x in string]

print(string)