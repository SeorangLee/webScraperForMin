from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re
import csv

option = Options()
# option.add_argument("disable-infobars")
# option.add_argument("disable-extensions")
# #option.add_argument("start-maximized")
# option.add_argument('disable-gpu')
# option.add_argument('headless')

driver = webdriver.Chrome(r"C:\chromedriver.exe", options=option)


driver.implicitly_wait(3)
driver.get('http://www.enuri.com/')
WebDriverWait(driver, 10).until(
  EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="header-sr"]/div[1]"""))
)

elm_search = driver.find_element(By.XPATH, """//*[@id="search_keyword"]""")
elm_search.send_keys('삼성 냉장고')
btn_search = driver.find_element(By.XPATH, """//*[@id="header-sr"]/div[1]/span[2]""")
btn_search.click()


WebDriverWait(driver, 10).until(
  EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]"""))
)
# prices = soup.select('goods-cont type--list')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# print(html)
prices = soup.select('.tx--price')
print(len(prices))
# print(prices.get_text())
for p in prices:
  print(p.text)


