

"""
一些事项
1.自动登录 selenium
判断当前有没有登录，有就直接打开 没有就需要登录
2.抢票操作

"""
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
# 实现记录和读取cookie
import pickle

# 大麦网首页
damai_url = 'https://www.damai.cn/'
# 登录
login_url = 'https://passport.damai.cn/login'
# 抢票页面
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.57304d15Q2tfhR&id=733193814511&clicktitle=%E9%BB%84%E9%BE%84%E3%80%90%E6%9C%89%E6%B2%A1%E6%9C%89%E5%90%83%E8%BF%87%E9%A5%AD%E3%80%91LIVEHOUSE%E5%B7%A1%E6%BC%94%E2%80%94%E5%8C%97%E4%BA%AC%E7%AB%99'

# 大麦账密
userName = '13110512792'
userPwd = 'filang123'

# 大麦网抢票爬虫
class Concert:
    """初始化加载"""
    def __init__(self):
        self.status = 0   # 状态，表示当前操作到了哪个步骤
        self.login_method = 1   # {0: 模拟登陆， 1： cookie登录}
        self.driver = webdriver.Edge()
        self.driver.implicitly_wait(10)

    """登录网站 cookie用于记录用户信息"""
    def set_cookies(self):
        self.driver.get(login_url)
        print("###请登录###")

        # 输入账号密码 账密登录模块
        # self.driver.switch_to.frame('alibaba-login-box')
        # name = self.driver.find_element(By.ID, 'fm-login-id')
        # name.send_keys(userName)
        # self.driver.find_element(By.ID, 'fm-login-password').send_keys(userPwd)
        #
        # # 定位滑块元素
        # slider = self.driver.find_element(By.ID, 'nc_1_n1z')
        #
        # time.sleep(5)
        #
        # slider_location = slider.location
        # slider_size = slider.size
        # distance = slider_size['width']
        # print('### 即将开始拖曳滑块 ###')
        # print('distance' + distance)
        # # 滑动滑块到最右侧
        # ActionChains(self.driver).click_and_hold(slider).move_by_offset(distance, 0).release().perform()

        # 点击扫码登录
        self.driver.switch_to.frame('alibaba-login-box')
        qrCodeTab = self.driver.find_element(By.CSS_SELECTOR, 'div#login-tabs > div:nth-child(3)')
        qrCodeTab.click()

        self.driver.switch_to.default_content()
        # for sec in range(1, 30):
        #     print('### 剩余登录时间：' + str(30-sec) + '秒 ###')
        time.sleep(45)  # 简单处理 后续优化

        print("###登陆成功###")
        # 设置cookie cookie.pkl
        pickle.dump(self.driver.get_cookies(), open('cookies.pkl', 'wb'))
        print("###cookie保存成功###")
        # 跳转到抢票界面
        self.driver.get(target_url)

    # 如果当前我已经有了cookie.pkl
    def get_cookie(self):
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            print(cookie)
            # 构建cookies字典
            cookie_dict = {
                'domain': '.damai.cn',
                'name': cookie.get('name'),
                'value': cookie.get('value')
            }
            self.driver.add_cookie(cookie_dict)
        print('### 载入cookie成功 ###')
        # self.driver.refresh()

    """登录"""
    def login(self):
        # 执行登录操作
        if self.login_method == 0:
            self.driver.get(login_url)
        elif self.login_method == 1:
            print('###cookie登录方式###')
            # 如果当前目录下没有cookie.pkl这个文件
            if not os.path.exists('cookies.pkl'):
                print('###没有cookie.pkl文件###')
                # 登录一下 登录信息的记录
                self.set_cookies()
            else:
                print('###跳转去抢票页面###')
                self.driver.get(target_url)
                # 登录一下 通过selenium传入登录信息
                self.get_cookie()

    # 打开浏览器
    def enter_concert(self):
        print("###打开浏览器，进入抢票页面")
        # login
        self.login()
        self.driver.refresh()
        self.status = 2
        print("###登陆成功###")
        self.choose_ticket()

    # 抢票并且下单
    """"选票操作"""
    def choose_ticket(self):
        # 检查页面信息 判断是否有票
        print('')
        if self.status == 2:
            print('### 开始日期选择及票价选择 ###')
            # 寻找按钮
            while self.driver.title.find('确认订单') == -1:
                # 寻找下单按钮  先检查是否是二维码购买
                try:
                    scan_buy = self.driver.find_element(By.CSS_SELECTOR, 'div.scan-buy > div.qrcode-wrapper > div.buy-link')
                    print('元素存在')
                    scan_buy.click()
                except NoSuchElementException:
                    print('元素不存在')

                # 寻找下单按钮
                buybutton = self.driver.find_element(By.CSS_SELECTOR, 'div.buybtn')
                if buybutton.text == '提交缺货登记':
                    self.driver.refresh()
                elif buybutton.text == '选座购买':
                    self.status = 4
                elif buybutton.text == '立即购买':
                    buybutton.click()
                else:
                    self.status = 100
                title = self.driver.title
                if title == '选座购买':
                    self.status = 10
                elif title == '确认订单':
                    self.check_order()

    def check_order(self):
        print('订单确认')

if __name__ == '__main__':
    print('运行')
    con = Concert()
    con.enter_concert()