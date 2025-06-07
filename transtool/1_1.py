import os

def _load_dictionary(filepath):
    """
    Tải từ điển từ một file.

    Args:
        filepath (str): Đường dẫn đến file từ điển (format: CH=VI).

    Returns:
        tuple: (dict_data, max_phrase_len_in_dict)
    """
    dict_data = {}
    max_len = 0
    if not os.path.exists(filepath):
        print(f"Cảnh báo: Không tìm thấy file từ điển '{filepath}'.")
        return dict_data, max_len

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
    return dict_data, max_len

def translate_chinese_string(
    input_str,
    main_name_file='main_names.txt',
    sub_name_file='sub_names.txt',
    vietphrase_file='Vietphrase_new.txt'
):
    """
    Dịch một chuỗi tiếng Trung sang tiếng Việt dựa trên hệ thống từ điển ưu tiên.

    Args:
        input_str (str): Chuỗi tiếng Trung cần dịch.
        main_name_file (str): Đường dẫn đến file từ điển tên chính (ưu tiên 1).
        sub_name_file (str): Đường dẫn đến file từ điển tên phụ (ưu tiên 2).
        vietphrase_file (str): Đường dẫn đến file từ điển Vietphrase (ưu tiên 3).

    Returns:
        str: Chuỗi đã được dịch.
    """

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
    main_name_dict, max_main_len = _load_dictionary(main_name_file)
    sub_name_dict, max_sub_len = _load_dictionary(sub_name_file)
    phrase_dict, max_phrase_len = _load_dictionary(vietphrase_file)

    # Tính toán độ dài cụm từ tối đa từ tất cả các từ điển
    overall_max_phrase_len = max(max_main_len, max_sub_len, max_phrase_len, 1) # Đảm bảo ít nhất là 1

    # 3. Phân đoạn (Segmentation) chuỗi
    segmented_phrases = []
    i = 0
    n = len(processed_str)

    while i < n:
        found_match = False
        # Cố gắng tìm cụm từ dài nhất bắt đầu từ vị trí 'i'
        # Duyệt từ độ dài tối đa xuống 1
        for length in range(min(overall_max_phrase_len, n - i), 0, -1):
            sub_string = processed_str[i : i + length]

            # Kiểm tra cụm từ theo thứ tự ưu tiên
            if sub_string in main_name_dict or \
               sub_string in sub_name_dict or \
               sub_string in phrase_dict:
                
                # Thêm cụm từ tiếng Trung gốc vào danh sách phân đoạn
                # Việc dịch sẽ được thực hiện sau, với logic ưu tiên
                segmented_phrases.append(sub_string)
                i += length
                found_match = True
                break # Đã tìm thấy cụm từ dài nhất, thoát khỏi vòng lặp 'length'
        
        if not found_match:
            # Nếu không tìm thấy cụm từ nào trong bất kỳ từ điển nào (kể cả ký tự đơn lẻ),
            # thì thêm ký tự hiện tại vào danh sách và tiến lên 1 vị trí.
            # Điều này xử lý cả các ký tự không phải tiếng Trung (dấu câu, chữ Latin)
            # và các ký tự tiếng Trung không có trong từ điển.
            segmented_phrases.append(processed_str[i])
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
        
        # Giữ nguyên chữ hoa cho các ký tự không phải tiếng Trung hoặc không có trong từ điển
        # Logic này chủ yếu áp dụng cho các ký tự tiếng Anh/Latin hoặc dấu câu
        # Đối với tiếng Trung, casing được lấy từ từ điển đã quy định
        # Hiện tại, nếu segment không có trong dict, nó vẫn là segment gốc (VD: "A")
        # và casing của nó sẽ được giữ nguyên khi đưa vào result.
        # Nếu muốn xử lý phức tạp hơn cho tiếng Anh (ví dụ: "abc" -> "Abc" nếu "abc" không có trong dict)
        # thì cần một hàm is_english() và xử lý casing riêng.
        # Nhưng với yêu cầu giữ nguyên casing "nếu có" thì logic hiện tại đã bao phủ tốt.
        
        translated_segments.append(translation)
    
    # Ghép nối các phần đã dịch với dấu cách
    result = ' '.join(translated_segments)

    # 5. Hậu xử lý: Làm sạch các dấu cách thừa xung quanh dấu câu và chuẩn hóa
    result = result.replace(' ,', ',')
    result = result.replace(' .', '.')
    result = result.replace(' !', '!')
    result = result.replace(' ?', '?')
    result = result.replace(' :', ':')
    result = result.replace(' ;', ';')
    result = result.replace(' (', '(')
    result = result.replace(' )', ')')
    result = result.replace(' "', '"') # Xử lý dấu ngoặc kép
    result = result.replace('" ', '"') # Xử lý dấu ngoặc kép
    result = result.replace('\' ', "'")
    result = result.replace(' \'', "'")

    result = result.replace('  ', ' ') # Loại bỏ các khoảng trắng kép
    result = result.strip() # Loại bỏ khoảng trắng ở đầu và cuối chuỗi

    return result

# --- Sử dụng chương trình ---
str_to_translate = " 大奉京兆府，监牢. 牢. A."

# --- Tạo các file từ điển giả định để kiểm tra ---
# (Bạn cần đảm bảo các file này có nội dung tương ứng để thấy hiệu quả)

# 1. main_names.txt (Ưu tiên cao nhất)
if not os.path.exists('main_names.txt'):
    with open('main_names.txt', 'w', encoding='utf-8') as f:
        f.write("大奉=Đại Phụng Triều\n") # Override Vietphrase
        f.write("京兆府=Kinh Triệu Phủ Chính\n") # Override Vietphrase
        f.write("监牢=Giám Lao Lớn\n") # Override Vietphrase

# 2. sub_names.txt (Ưu tiên trung bình)
if not os.path.exists('sub_names.txt'):
    with open('sub_names.txt', 'w', encoding='utf-8') as f:
        f.write("大奉=Đại Phụng Quốc\n") # Bị main_names override
        f.write("京兆府=Kinh Triệu Phủ\n") # Sẽ được dùng nếu main_names không có
        f.write("牢=nhà lao\n") # Override Vietphrase

# 3. Vietphrase_new.txt (Ưu tiên thấp nhất)
if not os.path.exists('Vietphrase_new.txt'):
    with open('Vietphrase_new.txt', 'w', encoding='utf-8') as f:
        f.write("大奉=Đại Phụng\n")
        f.write("京兆府=Kinh Triệu phủ\n")
        f.write("监牢=giám lao\n")
        f.write("牢=lao\n")
        f.write("监=giám\n")
        f.write("京兆=Kinh Triệu\n") # Thêm từ ngắn hơn để test longest-match

# --- Chạy dịch ---
print(f"Chuỗi gốc: '{str_to_translate}'")
translated_text = translate_chinese_string(str_to_translate)
print(f"Chuỗi đã dịch: '{translated_text}'")
# Kết quả mong đợi: 'Đại Phụng Triều Kinh Triệu Phủ Chính, Giám Lao Lớn. nhà lao. A.'
# (Lưu ý: "监牢" được dịch thành "Giám Lao Lớn" từ main_names.txt)
# (Lưu ý: "牢" được dịch thành "nhà lao" từ sub_names.txt vì main_names không có, và sub_names ưu tiên hơn Vietphrase)

print("\n--- Test với chuỗi khác ---")
str_test2 = "这是一个测试，你好吗？A test."
# Thêm dữ liệu vào Vietphrase_new.txt (dùng 'a' để append)
if os.path.exists('Vietphrase_new.txt'):
    with open('Vietphrase_new.txt', 'a', encoding='utf-8') as f:
        f.write("这=Đây\n")
        f.write("是=là\n")
        f.write("一个=một\n")
        f.write("测试=kiểm tra\n")
        f.write("你好=Chào bạn\n")
        f.write("吗=không\n")

print(f"Chuỗi gốc: '{str_test2}'")
translated_text2 = translate_chinese_string(str_test2)
print(f"Chuỗi đã dịch: '{translated_text2}'")
# Kết quả mong đợi: 'Đây là một kiểm tra, Chào bạn không? A test.'

print("\n--- Test với các trường hợp ưu tiên ---")
str_test3 = "我的名字叫大奉，他在京兆府."
# Giả sử trong main_names.txt có:
# 大奉=Đại Phụng Vương
# Giả sử trong sub_names.txt có:
# 大奉=Đại Phụng Tộc
# Vietphrase_new.txt có:
# 大奉=Đại Phụng
# Kết quả mong đợi cho "大奉": "Đại Phụng Vương"
# Kết quả mong đợi cho "京兆府": "Kinh Triệu Phủ Chính" (từ main_names.txt)

if os.path.exists('main_names.txt'):
    with open('main_names.txt', 'a', encoding='utf-8') as f:
        f.write("我的=tên ta\n")
        f.write("名字=tên\n")
        f.write("叫=tên là\n")
        f.write("他在=hắn ở\n")
        f.write("大奉=Đại Phụng Vương\n") # Để kiểm tra ưu tiên

if os.path.exists('sub_names.txt'):
    with open('sub_names.txt', 'a', encoding='utf-8') as f:
        f.write("大奉=Đại Phụng Tộc\n") # Sẽ bị main_names override

if os.path.exists('Vietphrase_new.txt'):
    with open('Vietphrase_new.txt', 'a', encoding='utf-8') as f:
        f.write("我的=của tôi\n")
        f.write("名字=danh tự\n")
        f.write("叫=gọi\n")
        f.write("他在=hắn tại\n")
        f.write("大奉=Đại Phụng\n")


print(f"Chuỗi gốc: '{str_test3}'")
translated_text3 = translate_chinese_string(str_test3)
print(f"Chuỗi đã dịch: '{translated_text3}'")
# Kết quả mong đợi: 'tên ta tên là Đại Phụng Vương, hắn ở Kinh Triệu Phủ Chính.'
# Hoặc tương tự tùy vào từ điển của bạn.