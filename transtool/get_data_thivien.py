import requests
from bs4 import BeautifulSoup
import json


def make_data(old):
    new = old.replace('\n', '.')
    new = new.replace(',', '.')
    for i in range(10):
        new = new.replace(str(i), '')
    new = new.split('.')
    new = [x.strip() for x in new]
    new = [x.replace('  ', '') for x in new]
    new = [x for x in new if x]
    return new



url = "https://hvdic.thivien.net/whv/%E4%B8%80"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
hv_p = soup.find_all("p", {"class": "hvres-spell"})
for i in hv_p:
    hv = i.get_text()
dict = soup.find_all("div", {"class": "hvres-meaning han-clickable"})

pt = dict[0].get_text()
pt = make_data(pt)  

td = dict[1].get_text()
td = make_data(td)

tc = dict[2].get_text()
tc = make_data(tc)

tvc = dict[3].get_text()
tvc = make_data(tvc)

nqh = dict[4].get_text()
nqh = make_data(nqh)

data = {
    'Hán Việt': hv,
    'Phổ Thông': pt,
    'Trích Dẫn': td,
    'Thiều Chửu': tc,
    'Trần Văn Chánh': tvc,
    'Nguyễn Quốc Hùng': nqh,
}
with open('dict_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
tg_div = soup.find("div", {"class": "hvres-meaning han-clickable small"})
tg_a = tg_div.find_all('a')
for i in tg_a:
    print('https://hvdic.thivien.net' + i['href'])