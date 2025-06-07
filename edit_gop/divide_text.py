import re
with open ('text.txt', 'r', encoding="utf-8") as f:
    text = f.readlines()
file_names = []
#đến dòng nào bắt đầu bằng chữ chương thì ghi vào file mới
for line in text:
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    pattern = r"^Chương\s+\d+"
    line = line.strip()
    if not line:    
        continue
    if re.match(pattern, line):
        chapter_title = line
        chapter_title = re.sub(r'[\\/:*?"<>|]', ' ', chapter_title)
        filename = f"{chapter_title}.txt"
        filename = re.sub(r'[\\/:*?"<>|]', ' ', filename)
        with open(f"output/{filename}", "w", encoding="utf-8") as chapter_file:
            chapter_file.write(f"{chapter_title}\n\n")
        file_names.append(filename)
    else:
        if file_names:
            with open(f"output/{file_names[-1]}", "a", encoding="utf-8") as chapter_file:
                chapter_file.write(f"{line}\n\n ")
    
