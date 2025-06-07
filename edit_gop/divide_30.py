import re

with open('test.txt', 'r', encoding="utf-8") as f:
    text = f.readlines()

file_names = []
chapter_counter = 0
file_counter = 1

for line in text:
    line = line.replace(' ,', ',')
    line = line.replace(' .', '.')
    pattern = r"^Chương\s+\d+"
    line = line.strip()

    if not line:    
        continue

    if re.match(pattern, line):
        chapter_counter += 1

        if chapter_counter == 1:
            filename = f"output/Part_{file_counter}.txt"
            file_names.append(filename)

        with open(filename, "a", encoding="utf-8") as chapter_file:
            chapter_file.write(f"{line}\n\n")

        if chapter_counter == 30:
            chapter_counter = 0
            file_counter += 1
    else:
        if file_names:
            with open(filename, "a", encoding="utf-8") as chapter_file:
                chapter_file.write(f"{line}\n\n")