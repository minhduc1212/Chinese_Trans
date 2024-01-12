#import modules selenium to translate from baidu
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import clipboard
import os

driver = webdriver.Chrome()
driver.get(url ="https://fanyi.baidu.com/#zh/vie/ssssss")
sleep(1)
text = driver.find_element(By.CLASS_NAME, "output-bd")
sleep(1)
print(text.text)