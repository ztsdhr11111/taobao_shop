from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import pymongo


    #设置浏览器，（无头模式）
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

    #请求淘宝页面
url = 'https://www.taobao.com'
browser.get(url)


    #获得搜索按钮，最大等待时间为10s
wait = WebDriverWait(browser, 10)
input_button = wait.until(EC.presence_of_element_located((By.ID, 'q')))

    #清空输入框
input_button.clear()

    #输入关键字
temp = input('请输入商品名称：')
input_button.send_keys(temp)
input_button.send_keys(Keys.ENTER)
    #链接数据库
MONGO_URL = 'localhost'
MONGO_DB = 'taobaoshop'
MONGO_COLLECTION = temp
client = pymongo.MongoClient(MONGO_URL)
db =client.MONGO_DB

 #保存到数据库
def save_info(shop_info):
    if db.MONGO_COLLECTION.insert(shop_info):
        print('保存成功')
    else:
        print('存储失败')

        
        
    #遍历商品每一页
for i in range(1, 101):
    print('当前页码：   ' + str(i) )
        #页码输入框
    input_yema = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'J_Input')))
    input_yema.clear()
    time.sleep(1)
    input_yema.send_keys(i)
    time.sleep(1)
    input_yema.send_keys(Keys.ENTER)
    time.sleep(1)
        #获取商品信息
    print('解析页面....')
    html = browser.page_source
    doc = pq(html)
    items = doc('.m-itemlist .items .item').items()
    for item in items:
        print('获得商品信息中.....')
        shop_info = {
                    'price':item.find('.price').text() ,
                    'title':item.find('.J_ClickStat').text(),
                    'deal':item.find('.deal-cnt').text(),
                    'shop':item.find('.shop').text(),
                    'location':item.find('.location').text(),
                    'img':item.find('.pic .img').attr('data-src'),
                     }
        
        print(shop_info)
        save_info(shop_info)
        time.sleep(5)
    
   
    
