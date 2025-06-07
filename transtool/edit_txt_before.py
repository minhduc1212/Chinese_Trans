with open('test.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
content = ''
for data in data:
    if data != '\n':
        data = data.strip()
        data = data.replace("，", ",")
        data = data.replace("。", ".")
        data = data.replace("、", ",")
        data = data.replace("；", ";")
        data = data.replace("：", ":")
        data = data.replace("？", "?")
        data = data.replace("！", "!")
        data = data.replace("（", "(")
        data = data.replace("）", ")")
        data = data.replace("【", "[")
        data = data.replace("】", "]")
        data = data.replace("《", "<")
        data = data.replace("》", ">")
        content += data + '\n'
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write(content)