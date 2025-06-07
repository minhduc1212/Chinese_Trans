import requests
import re
import json

#Đọc file txt
content = ''
with open('test.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
    for text in data:
        text = text.strip()
        text = text.replace('。', '.')
        text = text.replace('，', ',')
        text = text.replace('“', '"')
        text = text.replace('”', '"')
        text = text.replace('‘', "'")
        text = text.replace('’', "'")
        text = text.replace('；', ';')
        # Địa chỉ URL của dịch vụ
        url = 'https://fanyi.baidu.com/ait/text/translate'
        headers= {'Content-Type': 'application/json'}

        # Dữ liệu gửi đi dưới dạng JSON
        data = {
            "query": text,
            "from": "zh",
            "to": "vie",
            "reference": "",
            "corpusIds": [],
            "qcSettings": ["1","2","3","4","5","6","7","8","9","10","11"],
            "domain": "common"
        }

        # Thực hiện yêu cầu POST
        response = requests.post(url, json=data, headers=headers)

        data_response =[]
        # Kiểm tra mã trạng thái HTTP
        if response.status_code == 200:
            #lấy tất cả các str trong {} và cho vào data_response tạo thành danh sách json
            #thêm "}" vào cuối chuỗi để tránh lỗi
            data_response = re.findall(r'\{.*?\}', response.content.decode('utf-8'))

        else:
            # Xử lý lỗi nếu có
            print("Error:", response.status_code)

        for i in data_response: 
            i = i + "}" + "}"
            i = i.replace("[", "")
            i = i.replace("]", "")
            if "dst" in i:
                try:
                    i = json.loads(i)
                    print(i["data"]["list"]["dst"])
                    content += i["data"]["list"]["dst"] + '\n'
                except:
                    print("Error in", text)
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write(content)
    f.flush()