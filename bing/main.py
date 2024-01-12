from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import clipboard

# Khởi tạo trình duyệt Chrome
browser = webdriver.Chrome()

# Mở trang web Bing Translator
browser.get('https://www.bing.com/translator')

# Đợi trang web tải xong
sleep(5)

# Tìm phần tử nhập văn bản
text_input = browser.find_element(By.ID, 'tta_input_ta')
text_input.clear()

# Gửi văn bản cần dịch
text_input.send_keys("Hello, how are you?")

# Bấm phím Enter để bắt đầu dịch
text_input.send_keys(Keys.ENTER)

# Đợi trang web dịch xong
sleep(5)

element = browser.find_element(By.ID, 'tta_copyIcon')
element.click()

sleep(5)



# Đóng trình duyệt
browser.close()

text = clipboard.paste()
print(text)