import json

str = '鸟类=loài chim/loài lông vũ/vũ tộc'
str = str.split('=')
print(str[0])
str_vn=str[1].split('/')
print(str_vn)

data = {
    'ch': str[0],
    'vn': str_vn
}

print(data)
data_json = json.loads(json.dumps(data))
print('Json: ',data_json['ch'])

dict = {}
dict[str[0]] = str_vn
print('Dict: ',dict)
for key, value in dict.items():
    print('Dict: ',key)   
    for i in value:
        print('Dict: ',i)

