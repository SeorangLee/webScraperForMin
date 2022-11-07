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
import csv






option = Options()

#*IP 막혔을때
# option.add_argument("--proxy-server=socks5://127.0.0.1:9150")
# option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
# option.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
# torexe = os.popen(r'')
#*브라우저 키지 않고 작동
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
#option.add_argument("start-maximized")
option.add_argument('disable-gpu')
option.add_argument('headless')


driver = webdriver.Chrome(r"C:\chromedriver.exe", options=option)
driver.implicitly_wait(3)
driver.get('http://www.enuri.com/')


#*엑셀에서 상품코드 불러오기

# csvfilePath = 'C:/Users/SierraLee/Study/Croller/croller/croller/list.csv'
df = pd.read_csv('./list.csv')
# modelCodeList = ['삼성 냉장고', 'LG 에어컨']
modelCodeList = df['판매자상품코드'].tolist()
# print(modelCodeList)

#*상품코드별 최저가 검색 후 Data set 만들기
sleep(5)
WebDriverWait(driver, 1000).until(
  EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="search_keyword"]"""))
)



data = []
print(len(modelCodeList))
#* for문 여기서 부터 시작
for i in range(len(modelCodeList)):
  elm_search = driver.find_element(By.XPATH, """//*[@id="search_keyword"]""")
  data.append([modelCodeList[i]])
  elm_search.send_keys(modelCodeList[i])

  btn_search = driver.find_element(By.XPATH, """//*[@id="header-sr"]/div[1]/span[2]""")
  btn_search.click() 

  WebDriverWait(driver, 1000).until(
    EC.visibility_of_all_elements_located((By.XPATH, """//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]"""))
  )

  except_rental_checkbox = driver.find_element(By.XPATH, '//*[@id="chLPcondition1"]')

  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')
  prices1 = soup.select('.tx--price')
  prices2 = soup.select('.col--price>a>em')
  prices = prices1+ prices2
  driver.find_element(By.XPATH, '//*[@id="search_keyword"]').clear()
  sleep(0.2)

  priceList= []
  for p in prices :
    str = (p.text).replace(',', '')
    
    #* 중고, 렌탈 제외, 카드할인 포함 
    # if int(str) !=1 : 
    #   priceList.append(int(str))
      

  minPrice = min(priceList)
  data[i].append(minPrice)

  print(i+1)
print(data)


f = open('example.csv', 'w', newline='')
wr = csv.writer(f)
wr.writerows(data)
f.close()


