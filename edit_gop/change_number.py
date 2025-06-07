import re

# Đường dẫn đến tệp văn bản
file_path = "test.txt"

# Đọc nội dung của tệp văn bản
with open(file_path, "r", encoding='utf-8') as file:
    content = file.read()

# Tìm và thay thế các từ có dạng "Chương + 1 số"
pattern = r"(Chương \d+)"
print(re.findall(pattern, content))
"""with open("1.txt", "w", encoding='utf-8') as file:
    for i in re.findall(pattern, content):
        file.write(i + "\n")"""
replacement = lambda match: f"{match.group(1).split()[0]} {int(match.group(1).split()[1]) - 8}"
new_content = re.sub(pattern, replacement, content)

# Ghi nội dung đã được thay thế vào tệp văn bản
with open(file_path, "w", encoding='utf-8') as file:
    file.write(new_content)