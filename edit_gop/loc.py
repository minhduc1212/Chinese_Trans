with open("name.txt", "r", encoding="utf-8") as f:
    data = f.readlines()

names = ''
main_name_vi = 'Phương Minh'
main_name='方明=Phương Minh'
excluded_substrings = ['Khán', 'Dĩ Kinh', 'Tự Nhiên', main_name_vi, 'Giá Dã', 'Na', 'Dĩ', 'Cư Nhiên', 'Cánh', 'Cánh Nhiên', 'Dữ', 'Thì Bất', 'Chích', 'Chi', 'Bất', 'Giản Trực', '向问=', '在=', '都被=', '时也=', '大大咧=']

for line in data:
    line = line.strip()
    if not any(substring in line for substring in excluded_substrings):
        names += line + '\n'
    elif main_name_vi in line and line == main_name:
        names += line + '\n'

with open("name.txt", "w", encoding="utf-8") as f:
    f.write(names)