from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request 




# csvfilePath = 'C:/Users/SierraLee/Study/Croller/croller/croller/list.xls'
df = pd.read_excel('./list.xlsx')
modelCodeList = df['판매자상품코드'].tolist()
option = Options()
# option.add_argument("--proxy-server=socks5://127.0.0.1:9150")
# option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
# option.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
# option.add_argument("disable-infobars")
# option.add_argument("disable-extensions")
# #option.add_argument("start-maximized")
# option.add_argument('disable-gpu')
# option.add_argument('headless')
# torexe = os.popen(r'')
driver = webdriver.Chrome(r"C:\chromedriver.exe", options=option)


driver.implicitly_wait(3)
driver.get('http://www.enuri.com/')
sleep(5)
WebDriverWait(driver, 1000).until(
  EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="search_keyword"]"""))
)

elm_search = driver.find_element(By.XPATH, """//*[@id="search_keyword"]""")


# for i in range(modelCodeList.len) :
#   elm_search.send_keys(modelCodeList[i])
#   btn_search = driver.find_element(By.XPATH, """//*[@id="header-sr"]/div[1]/span[2]""")
#   btn_search.click()
#   WebDriverWait(driver, 10).until(
#     EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]"""))
#   )
#   html = driver.page_source
#   soup = BeautifulSoup(html, 'html.parser')
#   prices = soup.select('.tx--price')
#   print(len(prices))
#   for p in prices: #이 타이밍에서 list 만들고 그 안에서 최저가 찾아서 csv 업로드 필요
#     print(p.text)

elm_search.send_keys(modelCodeList[0])
btn_search = driver.find_element(By.XPATH, """//*[@id="header-sr"]/div[1]/span[2]""")
btn_search.click()


WebDriverWait(driver, 1000).until(
  EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]"""))
)
# prices = soup.select('goods-cont type--list')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# print(html)
prices1 = soup.select('.tx--price')
prices2 = soup.select('.col--price>a>em')
prices = prices1+ prices2

# print(type(prices2))

print(len(prices))
for p in prices:
  print(p.text)


