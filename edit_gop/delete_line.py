with open ('test.txt', 'r', encoding="utf-8") as f:
    text = f.readlines()
    for line in text:
        if 'donate' in line:
            text.remove(line)
with open ('test.txt', 'w', encoding="utf-8") as f:
    f.writelines(text)