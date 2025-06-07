def optimize_and_fix_chinese_phrase_extraction(input_str, vietphrase_file='Vietphrase_new.txt'):
    """
    Giải thích, tối ưu và sửa lỗi code để trích xuất và dịch cụm từ tiếng Trung trong chuỗi đầu vào.

    Args:
        input_str: Chuỗi đầu vào chứa tiếng Trung và các ký tự khác.
        vietphrase_file: Đường dẫn đến file Vietphrase_new.txt.

    Returns:
        Chuỗi kết quả đã được dịch và xử lý.
    """

    # Bước 1: Tiền xử lý chuỗi đầu vào
    input_str = input_str.replace('，', ',')
    input_str = input_str.replace('。', '.')

    # Bước 2: Đọc dữ liệu từ điển Vietphrase
    data_ch = set()
    phrase_dict = {}
    try:
        with open(vietphrase_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('=')
                if len(parts) == 2:  # Đảm bảo dòng có đúng định dạng "Chinese=Vietnamese"
                    ch, vi = parts
                    data_ch.add(ch)
                    phrase_dict[ch] = vi.split('/')[0] # Lấy phần đầu của bản dịch nếu có nhiều bản dịch
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file từ điển '{vietphrase_file}'. Vui lòng kiểm tra đường dẫn.")
        return input_str # Trả về chuỗi gốc nếu không tải được từ điển

    # Bước 3: Xác định vị trí các ký tự không phải tiếng Trung
    positions = [index for index, char in enumerate(input_str) if char not in data_ch]

    phrase_list = []
    start_index = 0 # Bắt đầu từ đầu chuỗi

    for pos in positions:
        # Trích xuất phần chuỗi tiếng Trung từ vị trí bắt đầu đến vị trí ký tự không phải tiếng Trung
        chinese_segment = input_str[start_index:pos]
        if chinese_segment: # Chỉ xử lý nếu segment không rỗng
            sub_phrase_list = []
            y_list = []
            segment_len = len(chinese_segment)
            for x in range(segment_len):
                if y_list and x < y_list[-1]:
                    continue
                for y in range(segment_len, x, -1): # Duyệt từ dài nhất đến ngắn nhất
                    phrase = chinese_segment[x:y]
                    if phrase in data_ch:
                        sub_phrase_list.append(phrase)
                        y_list.append(y)
                        break # Tìm thấy cụm từ dài nhất có thể, dừng vòng lặp y
                else: # Nếu không tìm thấy cụm từ nào bắt đầu từ x trong data_ch, coi ký tự đơn là một cụm từ
                    if chinese_segment[x] in data_ch: # Check single character as phrase
                        sub_phrase_list.append(chinese_segment[x])


            phrase_list.extend(sub_phrase_list)

        # Thêm ký tự không phải tiếng Trung vào phrase_list
        phrase_list.append(input_str[pos])
        start_index = pos + 1 # Cập nhật vị trí bắt đầu cho segment tiếp theo

    # Xử lý phần còn lại của chuỗi sau ký tự không phải tiếng Trung cuối cùng (nếu có)
    remaining_segment = input_str[start_index:]
    if remaining_segment: # Chỉ xử lý nếu segment không rỗng
        sub_phrase_list = []
        y_list = []
        segment_len = len(remaining_segment)
        for x in range(segment_len):
            if y_list and x < y_list[-1]:
                continue
            for y in range(segment_len, x, -1):
                phrase = remaining_segment[x:y]
                if phrase in data_ch:
                    sub_phrase_list.append(phrase)
                    y_list.append(y)
                    break
            else:
                if remaining_segment[x] in data_ch: # Check single character as phrase
                    sub_phrase_list.append(remaining_segment[x])
        phrase_list.extend(sub_phrase_list)


    # Bước 4: Dịch và ghép cụm từ
    translated_phrases = []
    for phrase in phrase_list:
        translated_phrase = phrase_dict.get(phrase, phrase) # Dịch nếu có trong từ điển, ngược lại giữ nguyên
        translated_phrases.append(translated_phrase)

    result = ' '.join(translated_phrases)

    # Bước 5: Hậu xử lý chuỗi kết quả (loại bỏ khoảng trắng thừa và chỉnh sửa dấu câu)
    result = result.replace(' .', '.').replace(' ,', ',').replace('  ', ' ').strip()
    result = result.replace(' !', '!').replace(' ?', '?') # Xử lý dấu chấm than và chấm hỏi
    result = result.replace(', .', ',.') # Xử lý trường hợp dấu phẩy và dấu chấm liền nhau do replace space
    result = result.replace('，', ',').replace('。', '.') # Đảm bảo không còn dấu phẩy, chấm câu tiếng trung sót lại (redundant but safe)


    return result

# Đoạn code gốc và test
str_input = "大奉京兆府，监牢. 牢. AB."
str_input = str_input.replace('，', ',') # dòng này có vẻ thừa vì đã replace ở hàm
str_input = str_input.replace('。', '.') # dòng này có vẻ thừa vì đã replace ở hàm
data_ch = set() # dòng này bị override trong hàm
phrase_dict = {} # dòng này bị override trong hàm

with open('Vietphrase_new.txt', 'r', encoding='utf-8') as f: # dòng này bị override trong hàm
    for line in f:
        ch, vi = line.strip().split('=')
        data_ch.add(ch)
        phrase_dict[ch] = vi.split('/')[0]


positions = [index for index, character in enumerate(str_input) if character not in data_ch] # dòng này bị override trong hàm

phrase_list = [] # dòng này bị override trong hàm
for p in range(0, len(positions)):
    y_list = []
    if p != 0:
        start = positions[p] - len(str_input[positions[p - 1]:positions[p]]) # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
        end = positions[p] # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
        for x in range(start, end + 1):
            if y_list and x < y_list[-1]:
                continue
            elif x == positions[p]:
                phrase_list.append(str_input[x]) # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
                continue
            for y in range(end, start, -1):
                if str_input[x:y] in data_ch: # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
                    phrase_list.append(str_input[x:y]) # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
                    y_list.append(y)
                    break

    elif p == 0:
        start = len(str_input[0:positions[0]]) - positions[0] # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
        end = len(str_input[0:positions[0]]) # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
        for x in range(start, end + 1):
            if y_list and x < y_list[-1]:
                continue
            elif x == positions[p]:
                phrase_list.append(str_input[x]) # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
                continue
            for y in range(end, start, -1):
                if str_input[x:y] in data_ch: # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
                    phrase_list.append(str_input[x:y]) # dòng này dùng lại str input đã replace ở ngoài, có vẻ không cần thiết
                    y_list.append(y)
                    break

result = ' '.join([phrase_dict.get(phrase, phrase) if phrase in phrase_dict else phrase for phrase in phrase_list]) # dòng này dùng lại phrase dict đã load ở ngoài

result = result.replace('，', ',') # redundant
result = result.replace(' .', '.')
result = result.replace(' ,', ',')
result = result.replace('  ', ' ')
result = result.replace(' !', '!')
result = result.replace(' ?', '?')
result = result.replace('  ', ' ') # redundant


print("Kết quả sau tối ưu và sửa lỗi:")
optimized_result = optimize_and_fix_chinese_phrase_extraction(str_input)
print(optimized_result)

print("\nKết quả code gốc:")
print(result)   