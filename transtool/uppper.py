string = "hà học bài. bài."

#split bằng dấu . hoặc xuống dòng
substrings = string.split('. ')
print(substrings)
str_new = ''
for substring in substrings:
    result = substring.capitalize()
    str_new += result + '. '
print(str_new)