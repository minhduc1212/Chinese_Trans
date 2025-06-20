import os
import re

def capitalize_after_punctuation(string):
    pattern = r'(?<=[.!?"])\s*(\w)'
    result = re.sub(pattern, lambda m: m.group(0)[:-1] + m.group(1).upper(), string)
    return result

def _load_dictionary(filepath):

    dict_data = {}
    max_len = 0
    if not os.path.exists(filepath):
        print(f"Cảnh báo: Không tìm thấy file từ điển '{filepath}'.")
        return dict_data

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue
                try:
                    ch_phrase, vi_translation = line.split('=', 1)
                    # Lấy phần dịch đầu tiên nếu có nhiều lựa chọn
                    dict_data[ch_phrase.strip()] = vi_translation.split('/')[0].strip()
                    if len(ch_phrase.strip()) > max_len:
                        max_len = len(ch_phrase.strip())
                except ValueError:
                    print(f"Cảnh báo: Dòng không đúng định dạng trong từ điển '{filepath}': '{line}'")
                    continue
    except Exception as e:
        print(f"Lỗi khi đọc file từ điển '{filepath}': {e}")
    return dict_data

def translate_chinese_string(
    input_str,
    main_name_file='main_names.txt',
    sub_name_file='sub_names.txt',
    vietphrase_file='Vietphrase_new.txt'
):


    # 1. Tiền xử lý chuỗi đầu vào: Chuẩn hóa dấu câu tiếng Trung sang tiếng Anh
    processed_str = input_str.replace('，', ',')
    processed_str = processed_str.replace('。', '.')
    processed_str = processed_str.replace('！', '!')
    processed_str = processed_str.replace('？', '?')
    processed_str = processed_str.replace('：', ':')
    processed_str = processed_str.replace('；', ';')
    processed_str = processed_str.replace('（', '(')
    processed_str = processed_str.replace('）', ')')
    processed_str = processed_str.replace('“', '"')
    processed_str = processed_str.replace('”', '"')
    processed_str = processed_str.replace('‘', "'")
    processed_str = processed_str.replace('’', "'")
    processed_str = processed_str.replace('…', '...') # Có thể chuẩn hóa thêm

    # 2. Tải và tổng hợp các từ điển
    main_name_dict = _load_dictionary(main_name_file)
    sub_name_dict = _load_dictionary(sub_name_file)
    phrase_dict= _load_dictionary(vietphrase_file)


    # 3. Phân đoạn (Segmentation) chuỗi
    segmented_phrases = []
    i = 0
    n = len(processed_str)

    while i < n:
        found_match = False
        # Cố gắng tìm cụm từ dài nhất bắt đầu từ vị trí 'i'
        # Duyệt từ độ dài tối đa xuống 1
        for length in range(n, i, -1):
            sub_string = processed_str[i : length]

            # Kiểm tra cụm từ theo thứ tự ưu tiên
            if sub_string in main_name_dict or \
               sub_string in sub_name_dict or \
               sub_string in phrase_dict:
                
                # Thêm cụm từ tiếng Trung gốc vào danh sách phân đoạn
                # Việc dịch sẽ được thực hiện sau, với logic ưu tiên
                segmented_phrases.append(sub_string)
                i = length
                found_match = True
                break 
        
        if not found_match:
            non_ch_phrase = ""
            while i < n and     processed_str[i] not in main_name_dict and \
                                processed_str[i] not in sub_name_dict and \
                                processed_str[i] not in phrase_dict:
                non_ch_phrase += input_str[i]
                i += 1
            if non_ch_phrase:
                segmented_phrases.append(non_ch_phrase)
            else:  
                i += 1

    # 4. Dịch các cụm từ đã phân đoạn theo thứ tự ưu tiên và ghép nối
    translated_segments = []
    for segment in segmented_phrases:
        translation = segment # Mặc định giữ nguyên nếu không tìm thấy
        
        # Thử dịch theo thứ tự ưu tiên
        if segment in main_name_dict:
            translation = main_name_dict[segment]
        elif segment in sub_name_dict:
            translation = sub_name_dict[segment]
        elif segment in phrase_dict:
            translation = phrase_dict[segment]
        
        translated_segments.append(translation)
    
    # Ghép nối các phần đã dịch với dấu cách
    result = ' '.join(translated_segments)

    # 5. Hậu xử lý: Làm sạch các dấu cách thừa xung quanh dấu câu và chuẩn hóa
    result = re.sub(r'[，. ]+', lambda m: m.group(0).replace('，', ',').replace(' .', '.').replace(' ,', ',').replace('  ', ' '), result)
    result = re.sub(r' [!?]', lambda m: m.group(0).replace(' !', '!').replace(' ?', '?'), result)

    return capitalize_after_punctuation(result)

# --- Sử dụng chương trình ---
str_to_translate = " 大奉京兆府，监牢. 牢. A."


# --- Chạy dịch ---
print(f"Chuỗi gốc: '{str_to_translate}'")
translated_text = translate_chinese_string(str_to_translate)
print(f"Chuỗi đã dịch: '{translated_text}'")

print("\n--- Test với chuỗi khác ---")
str_test2 = "这是一个测试，你好吗？A test."



print(f"Chuỗi gốc: '{str_test2}'")
translated_text2 = translate_chinese_string(str_test2)
print(f"Chuỗi đã dịch: '{translated_text2}'")


print("\n--- Test với các trường hợp ưu tiên ---")
str_test3 = "我的名字叫大奉，他在京兆府."




print(f"Chuỗi gốc: '{str_test3}'")
translated_text3 = translate_chinese_string(str_test3)
print(f"Chuỗi đã dịch: '{translated_text3}'")
# Kết quả mong đợi: 'tên ta tên là Đại Phụng Vương, hắn ở Kinh Triệu Phủ Chính.'
# Hoặc tương tự tùy vào từ điển của bạn.