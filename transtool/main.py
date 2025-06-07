import re

def capitalize_after_punctuation(string):
    return string.capitalize()

def optimize_and_fix_chinese_phrase_extraction_v2(input_str, vietphrase_file='Vietphrase_new.txt'):
    """
    Giải thích, tối ưu và sửa lỗi code để trích xuất và dịch cụm từ tiếng Trung,
    gom các từ không có trong data_ch nối tiếp nhau thành một cụm.
    """
    input_str = input_str.replace('，', ',').replace('。', '.')

    data_ch = set()
    phrase_dict = {}
    try:
        with open(vietphrase_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    ch, vi = parts
                    data_ch.add(ch)
                    phrase_dict[ch] = vi.split('/')[0]
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file từ điển '{vietphrase_file}'.")
        return input_str

    phrase_list = []
    i = 0
    n = len(input_str)
    while i < n:
        found_phrase = False
        for j in range(n, i, -1):
            phrase = input_str[i:j]
            if phrase in data_ch:
                phrase_list.append(phrase)
                i = j
                found_phrase = True
                break
        if not found_phrase:
            # Xử lý trường hợp ký tự hoặc cụm ký tự không có trong data_ch
            non_ch_phrase = ""
            while i < n and input_str[i] not in data_ch:
                non_ch_phrase += input_str[i]
                i += 1
            if non_ch_phrase:
                phrase_list.append(non_ch_phrase)
            else: # Trường hợp này có thể xảy ra nếu vòng lặp trước đó đã tăng i lên n
                i += 1 # Để đảm bảo tiến trình, mặc dù về lý thuyết không cần thiết

    result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list])

    result = re.sub(r'[，. ]+', lambda m: m.group(0).replace('，', ',').replace(' .', '.').replace(' ,', ',').replace('  ', ' '), result)
    result = re.sub(r' [!?]', lambda m: m.group(0).replace(' !', '!').replace(' ?', '?'), result)

    return capitalize_after_punctuation(result)


# Đoạn code test
str_input = "大奉京兆府，监牢. 牢. AB. CDEF 心目中神豪第一文"
# str_input = "心目中神豪第一文 AB CDEF" # Test case chỉ có ký tự không phải tiếng trung ở cuối
# str_input = "AB CDEF 心目中神豪第一文" # Test case chỉ có ký tự không phải tiếng trung ở đầu
# str_input = "AB CDEF" # Test case chỉ có ký tự không phải tiếng trung
# str_input = "大奉京兆府，监牢. 牢." # Test case chỉ có tiếng trung

optimized_result_v2 = optimize_and_fix_chinese_phrase_extraction_v2(str_input)
print("Kết quả sau tối ưu và sửa lỗi (phiên bản 2):")
print(optimized_result_v2)