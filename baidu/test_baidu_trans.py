#import modules selenium to translate from baidu
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

paragraph = '雾霭沉沉的天空，挤压的的乌云层叠排开，阴冷的天气冰凉的秋风撕咬着大地，庄询提着酒坛，另一只手裹裹衣服，目光眺望大道。'
driver = webdriver.Chrome()
driver.get(url ="https://fanyi.baidu.com/mtpe-individual/multimodal#/zh/vie/") #https://fanyi.baidu.com/#zh/vie/ với class in put: textarea và output là class: output-bd
sleep(5)
#click to change language
change_language = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/div/span")
change_language.click()
sleep(5)

"""input_box = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div")
input_box.send_keys(paragraph)
sleep(5)
txt_div = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]")
print(txt_div.text)"""
