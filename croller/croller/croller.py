from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request 
import csv
import math






option = Options()

#*IP 막혔을때
# option.add_argument("--proxy-server=socks5://127.0.0.1:9150")
# option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
# option.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
# torexe = os.popen(r'')
#*headless 상태에서 checkbox click을 도와줌
# option.add_argument("window-size=1920,1080")
# #*브라우저 키지 않고 작동
option.add_argument('headless')
option.add_argument("start-maximized")
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')


driver = webdriver.Chrome(options=option, service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(r"C:\chromedriver.exe", options=option)
driver.implicitly_wait(3)
driver.get('http://www.enuri.com/')


#*엑셀에서 상품코드 불러오기


df = pd.read_csv('./list.csv')
modelCodeList = df['판매자상품코드'].tolist()

#*상품코드별 최저가 검색 후 Data set 만들기
sleep(0.3)
WebDriverWait(driver, 1000).until(
  EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="search_keyword"]"""))
)


data = []
print("The number of models " + str(len(modelCodeList)))
#* for문 여기서 부터 시작
for i in range(len(modelCodeList)):
  data.append([modelCodeList[i]])
  elm_search = driver.find_element(By.XPATH, """//*[@id="search_keyword"]""")
  elm_search.send_keys(modelCodeList[i])

  btn_search = driver.find_element(By.XPATH, """//*[@id="header-sr"]/div[1]/span[2]""")
  btn_search.click() 
  sleep(0.3)

  first_product = driver.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]/ul/li[1]/div/div[1]')
  first_product.click()
  sleep(0.3)

  driver.switch_to.window(driver.window_handles[1])
  btn_card_discount = driver.find_element(By.XPATH, '//*[@id="prod_pricecomp"]/div[1]/div/div[2]/div[2]/label')
  btn_card_discount.click()
  sleep(0.2)

  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')

  price1 = soup.select(".comparison__rt>.cont__box>.comprod__list>.comprod__item>.col>.pinfo__group>.line__price>.tx_cardprice>a>em")
  price2 = soup.select(".comparison__rt>.cont__box>.comprod__list>.comprod__item>.col.col--rt>.pinfo__group>.line__price>a>em")

  prices = price1 + price2
 
  priceList= []
  for p in prices :
    price_str = (p.text).replace(',', '')
    priceList.append(int(price_str))
  
  minPrice = min(priceList)
  data[i].append(minPrice)
  process_percent = math.trunc(((i+1)/len(modelCodeList))*100)
  print(str(process_percent) + '%')
  driver.close()
  driver.switch_to.window(driver.window_handles[0])
  driver.find_element(By.XPATH, '//*[@id="search_keyword"]').clear()
  sleep(0.2)

print(data)


f = open('example.csv', 'w', newline='')
wr = csv.writer(f)
wr.writerows(data)
f.close()


