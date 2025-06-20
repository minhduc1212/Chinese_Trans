import re

def capitalize_first_and_after_punctuation(string_input): # Đổi tên tham số để tránh trùng tên với kiểu 'str'
    if not string_input: # Xử lý trường hợp chuỗi rỗng
        return ""

    processed_string = string_input[0].upper() + string_input[1:]

    pattern = r'(?<=[.!?"])\s*(\w)'


    result = re.sub(pattern, lambda m: m.group(0)[:-1] + m.group(1).upper(), processed_string)

    return result

# Chuỗi ví dụ từ bạn
input_str = 'hello world. this is a test! "let\'s see how it works."'
output_str = capitalize_first_and_after_punctuation(input_str)
print(f"Original: '{input_str}'")
print(f"Modified: '{output_str}'")
# Kết quả mong muốn: 'Hello world. This is a test! "Let's see how it works."'

