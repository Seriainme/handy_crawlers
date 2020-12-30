from selenium import webdriver
import  urllib.request
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import  random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from lxml import etree

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/64.0.3282.140 Safari/537.36"
options.add_argument('User-Agent=%s' % user_agent)
options.add_argument('disable-infobars')
options.add_argument('--disable-gpu')
# 开发者模式
options.add_experimental_option('excludeSwitches', ['enable-automation'])
chromedriver = "D:/Python/chromedriver.exe"
driver = webdriver.Chrome(chromedriver,chrome_options=options)
actions = ActionChains(driver)


def down_all_songsof1(singer_url):
 driver.get(singer_url+'/tracks')
 html_data = etree.HTML(driver.page_source)
 result_songurls=html_data.xpath('/html/body/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/div/ul//div/div/div[1]/a/@href')
 for result_songurl in result_songurls:
  if len(str(result_songurl).split('/'))==3 :
   print('seen: '+result_songurl)
   down_single('https://soundcloud.com'+result_songurl)

 # print('https://soundcloud.com'+song_url)
  #down_single('https://soundcloud.com'+song_url)


def down_single(song_url):
 data=driver.get('https://www.klickaud.co/')
 driver.find_element_by_xpath('//*[@id="header"]/div/div[1]/div[1]/form/input[1]')
 element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div[1]/div[1]/form/input[1]')))
 driver.find_element_by_xpath('//*[@id="header"]/div/div[1]/div[1]/form/input[1]').send_keys(song_url)
 driver.find_element_by_xpath('//*[@id="btn"]').click()
 downloadLink = driver.find_element_by_xpath('//*[@id="header"]/div/div/div[1]/div/div[3]/table/tbody/tr/td[2]/a').get_attribute("href")
 print( downloadLink)
 path = os.getcwd()
 singer_n=str(song_url).split('/')[-2].replace('-',' ')
 print('singer name :'+singer_n)
 song_n=str(song_url).split('/')[-1].replace('-',' ')
 try:
  if not os.path.exists(path+ singer_n ):
    os.makedirs(os.path.join(path,singer_n ))
 except Exception as e:
  print(e)
 urllib.request.urlretrieve(url=downloadLink ,filename=os.path.join(path,singer_n)+'/{}.mp3'.format(song_n ),)



#down_single('emmanuelle-garda','je-danse')

# get_all_songnames('emmanuelle-garda')
# down_single('https://soundcloud.com/emmanuelle-garda/sur-le-pas-de-ta-porte')

down_all_songsof1('https://soundcloud.com/emmanuelle-garda')

driver.close()
