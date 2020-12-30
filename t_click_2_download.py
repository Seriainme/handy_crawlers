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
import  requests
import  time

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/64.0.3282.140 Safari/537.36"
options.add_argument('User-Agent=%s' % user_agent)
options.add_argument('disable-infobars')
options.add_argument('--disable-gpu')
# 开发者模式
options.add_experimental_option('excludeSwitches', ['enable-automation'])
#选择文件下载位置
prefs={'download.default_directory': 'D:/app/sound'}
options.add_experimental_option('prefs', prefs)

chromedriver = "D:/Python/chromedriver.exe"
driver = webdriver.Chrome(chromedriver,chrome_options=options)
actions = ActionChains(driver)

def down_single(song_url):
    data=driver.get('https://www.klickaud.co/')
    driver.find_element_by_xpath('//*[@id="header"]/div/div[1]/div[1]/form/input[1]')
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div[1]/div[1]/form/input[1]')))

    driver.find_element_by_xpath('//*[@id="header"]/div/div[1]/div[1]/form/input[1]').send_keys(song_url)
    driver.find_element_by_xpath('//*[@id="btn"]').click()

    driver.find_element_by_xpath('//*[@id="dlMP3"]').click()
    time.sleep(20)
    save_info=driver.find_element_by_xpath('//*[@id="dlMP3"]').text
    print('save info1 : '+save_info)
    sleep_time=20

    while save_info=='DOWNLOAD THE SONG' or str(save_info)[0:6]=='SAVING':
        print('undone yet.')
        driver.find_element_by_xpath('//*[@id="dlMP3"]').click()
        start_t=time.time()
        sleep_time=sleep_time+10
        time.sleep(sleep_time)
        save_info=driver.find_element_by_xpath('//*[@id="dlMP3"]').text
        if  save_info=='Saved Successfully!':
            break
        end_t=time.time()
        print('time cost : %.5f sec' %(start_t-end_t))
        print('save info2 : '+save_info)

    sleep_time=20

    # downloadLink = driver.find_element_by_xpath('//*[@id="header"]/div/div/div[1]/div/div[3]/table/tbody/tr/td[2]/a').get_attribute("href")
    # print( downloadLink)
    # path = os.getcwd()
    # singer_n=str(song_url).split('/')[-2].replace('-',' ')
    # print('singer name :'+singer_n)
    # song_n=str(song_url).split('/')[-1].replace('-',' ')
    # try:
    #     if not os.path.exists(path+ singer_n ):
    #         os.makedirs(os.path.join(path,singer_n ))
    # except Exception as e:
    #     print(e)
    # urllib.request.urlretrieve(url=downloadLink ,filename=os.path.join(path,singer_n)+'/{}.mp3'.format(song_n ),)

down_single('https://soundcloud.com/synnrmusic/12-doom')
down_single('https://soundcloud.com/synnrmusic/10-yellow-tape')
down_single('https://soundcloud.com/emmanuelle-garda/ici')

driver.close()