import re
import tkinter as tk
import threading
from tkinter import ttk

def capitalize_after_punctuation(string):
    pattern = r'(?<=[.!?":“\n])\s*(\w)'
    result = re.sub(pattern, lambda m: m.group(0).upper(), string)
    return result

def run_data():
    data_ch = set()
    phrase_dict = {}

    with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f:
        for line in f:
            ch, vi = line.strip().split('=')
            data_ch.add(ch)
            phrase_dict[ch] = vi.split('/')[0]

    return data_ch, phrase_dict

def process(data_ch, phrase_dict):
    input_text = input_text_widget.get("1.0", tk.END).strip()
    input_text = input_text.replace("，", ",")
    input_text = input_text.replace("。", ".")
    input_text = input_text.replace("、", ",")
    input_text = input_text.replace("；", ";")
    input_text = input_text.replace("：", ":")
    input_text = input_text.replace("？", "?")
    input_text = input_text.replace("！", "!")
    input_text = input_text.replace("（", "(")
    input_text = input_text.replace("）", ")")
    input_text = input_text.replace("【", "[")
    input_text = input_text.replace("】", "]")
    input_text = input_text.replace("《", "<")
    input_text = input_text.replace("》", ">")


    positions = []
    characters = ['.', ',', '!', '?', ':', ';', '(', ')', '"', '“', '”', '\n', '=', '】', '【', '》', '《', '）', '（', '！', '？', '：', '；', '、', '。', '，', ' ']  
    for index, character in enumerate(input_text):
        if character in characters:
            positions.append(index)
    if input_text[-1] not in characters:
        positions.append(len(input_text))

    phrase_list = []
    for p in range(len(positions)):
        y_list = [] 
        if p != 0:
            start = positions[p - 1] 
            end = positions[p]
            for x in range(start + 1, end + 1):
                if x > input_text.index(input_text[-1]):
                    break
                if input_text[x] == ' ':
                    continue
                elif y_list and x < y_list[-1]:
                    continue
                elif x == positions[p]:
                    phrase_list.append(input_text[x])
                    continue
                for y in range(end, -1, -1):
                    if y_list and y < y_list[-1]:
                        break
                    elif input_text[x:y] in data_ch:
                        phrase_list.append(input_text[x:y])
                        y_list.append(y)
                        break
                    elif input_text[x] not in data_ch and input_text[y] not in data_ch :
                        if x == y or x == y - 1:
                            phrase_list.append(input_text[x])
                            y_list.append(y)
                            break
                        else:   
                            if len(input_text[x:y]) == 2:
                                phrase_list.append(input_text[x:y])
                                y_list.append(y)
                                break
                            else:
                                for index, i in enumerate(input_text[x+1:y]):
                                    if i not in data_ch and index == len(input_text[x+1:y-1]) - 1:
                                        phrase_list.append(input_text[x:y]) 
                                        y_list.append(y)
                                        break
                                    elif i not in data_ch and index < len(input_text[x+1:y-1]) - 1:
                                        continue
                                    else:
                                        break

        elif p == 0:
            end = positions[p]
            for x in range(0, end + 1):
                if x > input_text.index(input_text[-1]):
                    break
                if input_text[x] == ' ':
                    continue
                elif y_list and x < y_list[-1]:
                    continue
                elif x == positions[p]:
                    phrase_list.append(input_text[x])
                    continue
                for y in range(end, -1, -1):
                    if y_list and y < y_list[-1]:
                        break
                    elif input_text[x:y] in data_ch:
                        phrase_list.append(input_text[x:y])
                        y_list.append(y)
                        break
                    elif input_text[x] not in data_ch and input_text[y] not in data_ch :
                        if x == y or x == y - 1:
                            phrase_list.append(input_text[x])
                            y_list.append(y)
                            break
                        else:   
                            if len(input_text[x:y]) == 2:
                                phrase_list.append(input_text[x:y])
                                y_list.append(y)
                                break
                            else:
                                for index, i in enumerate(input_text[x+1:y]):
                                    if i not in data_ch and index == len(input_text[x+1:y-1]) - 1:
                                        phrase_list.append(input_text[x:y]) 
                                        y_list.append(y)
                                        break
                                    elif i not in data_ch and index < len(input_text[x+1:y-1]) - 1:
                                        continue
                                    else:
                                        break
    result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])

    result = result.replace('，', ',')
    result = result.replace(' .', '.')
    result = result.replace(' ,', ',')
    result = result.replace('  ', ' ')
    result = result.replace(' !', '!')
    result = result.replace(' ?', '?')

    result = capitalize_after_punctuation(result)
    output_text_widget.config(state=tk.NORMAL)
    output_text_widget.delete("1.0", tk.END)
    output_text_widget.insert(tk.END, result)
    output_text_widget.config()
    process_button.config(state=tk.NORMAL)  # Mở khóa nút xử lý sau khi hoàn thành xử lý

def process_text():
    process_button.config(state=tk.DISABLED)  # Khóa nút xử lý trong quá trình xử lý
    thread = threading.Thread(target=process, args=(data_ch, phrase_dict))
    thread.start()

# Create window
window = tk.Tk()
window.title("Chinese Trans Tool")

# Load data
data_ch, phrase_dict = run_data()

# Create widgets
input_text_widget = tk.Text(window, wrap=tk.WORD, width=40, height=10, font=("Times New Roman", 16), bg="#F5F5F5")
output_text_widget = tk.Text(window, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED, font=("Times New Roman", 16), bg="#F5F5F5")
process_button = ttk.Button(window, text="Dịch", command=process_text, style="Accent.TButton")

# Position widgets in the window
input_text_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
process_button.grid(row=0, column=1, padx=10, pady=10)
output_text_widget.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Configure resizing behavior
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=0)
window.columnconfigure(2, weight=1)
window.rowconfigure(0, weight=1)

# Apply a modern theme to the button
style = ttk.Style()
style.configure("Accent.TButton", font=("Segoe UI", 14))

# Run the window
window.mainloop()