import os

result_files = [file for file in os.listdir('E:/LT/Trans/output') if file.startswith('result')]

with open('E:/LT/Trans/result.txt', 'a', encoding='utf-8') as f:
    for file in result_files:
        with open(f'E:/LT/Trans/output/{file}', 'r', encoding='utf-8') as f1:
            f.write(f1.read())
            f.flush()