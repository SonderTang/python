# from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# 大麦抢票
driver = webdriver.Chrome()
# 浏览器最大化
driver.maximize_window()
# 打开网址
driver.get('https://www.damai.cn/')
# 充分加载
driver.implicitly_wait(10)
# 通过driver.execute()执行js代码 让页面滚动到底部
driver.execute_script("document.documentElement.scrollTop = document.documentElement.scrollHeight")

def searchKeyWord(keyw):
    # 找到输入框输入关键词 点击搜索
    inputEle = driver.find_element(By.CSS_SELECTOR, 'input.input')
    print(f'{keyw}')
    # send_keys中 \n 很重要
    inputEle.send_keys(keyw)
    driver.find_element(By.CSS_SELECTOR, 'a.search-btn').click()
    print(f'{keyw}搜索成功')
searchKeyWord('三上悠亚\n')
# time.sleep(2)
dataList = []

# 获取信息 同时点击切换到详情页面获取对应信息 目前收集五页数据
# for page in range(2):
#
#     uls = driver.find_elements(By.CSS_SELECTOR, '.job-list-box>li')
#     print(uls)




input()
