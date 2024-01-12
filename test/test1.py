string = "Hello"
#tìm vị trí của tta cả các kí tự l trong string
found = [i for i, ltr in enumerate(string) if ltr == 'l']
for f in found:
    print(f)

print(string[1])
print(string[2:4])
print(string[4-2:4])

#He/llo
string = string[0:2] + "/" + string[2:5]
#H/ello
string = string[0:1] + "/" + string[1:6]
print(string)
