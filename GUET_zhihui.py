from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import os


class BlogViewer:
    def __init__(self):
        # 初始化Edge浏览器选项
        self.options = webdriver.EdgeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # 初始化Edge浏览器
        self.driver = webdriver.Edge(options=self.options)


        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # 设置页面加载超时时间
        self.driver.set_page_load_timeout(30)

        # 基础URL
        self.base_url = "https://zhihui.guet.edu.cn/stu/News.aspx"

        # 直接设置cookie
        self.cookie_string = 'ASP.NET_SessionId=xxxxxxxxxxxxxxxxxx;sduuid=xxxxxxxxxxxxxxxxxxxx;T_Stu=userid=xxxxxxx;'#这里填入你的cookie，有几个就填几个，有的同学没有sduuid

    def set_cookies(self):
        """设置cookie"""
        try:
            # 先访问域名以设置cookie
            self.driver.get("https://zhihui.guet.edu.cn")
            time.sleep(2)

            # 解析cookie字符串
            cookies = {}
            for item in self.cookie_string.split(';'):
                if '=' in item:
                    key, value = item.strip().split('=', 1)
                    cookies[key] = value

            # 添加每个cookie
            for key, value in cookies.items():
                self.driver.add_cookie({
                    'name': key,
                    'value': value,
                    'domain': '.guet.edu.cn'
                })

            print("Cookie设置成功")
            return True
        except Exception as e:
            print(f"设置cookie时出错: {e}")
            return False

    def test_connection(self):
        """测试网络连接"""
        try:
            self.driver.get("https://www.baidu.com")
            print("网络连接正常")
            return True
        except Exception as e:
            print(f"网络连接测试失败: {e}")
            return False

    def random_scroll(self, duration=300):
        """
        随机滚动页面
        :param duration: 持续时间（秒）
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            # 随机滚动距离
            scroll_distance = random.randint(100, 500)
            # 随机滚动方向
            if random.random() > 0.5:
                self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            else:
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_distance});")

            # 随机等待时间
            time.sleep(random.uniform(1, 3))

            # 确保不会滚动到页面之外
            current_position = self.driver.execute_script("return window.pageYOffset;")
            if current_position < 0:
                self.driver.execute_script("window.scrollTo(0, 0);")

    def get_blog_links(self):
        """
        获取所有教案链接
        :return: 教案链接列表
        """
        try:
            print("正在获取教案链接...")
            self.driver.get(self.base_url)
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 打印页面源码以供调试
            print("页面加载成功，正在分析页面结构...")

            # 获取教案链接
            selector=".news-list a"
            links = []


            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"使用选择器 '{selector}' 找到 {len(elements)} 个链接")
                for element in elements:
                    link = element.get_attribute('href')
                    if link and ('Shownews.aspx' in link or 'news' in link):
                        links.append(link)
                    break

            if not links:
                print("未找到教案链接，尝试获取所有包含Shownews的链接...")
                elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'Shownews')]")
                for element in elements:
                    link = element.get_attribute('href')
                    if link:
                        links.append(link)

            print(f"总共找到 {len(links)} 个教案链接")
            return links

        except Exception as e:
            print(f"获取教案链接时出错: {e}")
            return []

    def view_blog(self, url):
        """
        查看单个教案
        :param url: 教案URL
        """
        try:
            print(f"正在访问: {url}")
            self.driver.get(url)

            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 随机滚动5分钟
            print("开始浏览文章（5分钟）...")
            self.random_scroll(300)

            # 滚动到页面顶部
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

        except Exception as e:
            print(f"浏览教案时出错: {e}")

    def run(self):
        """
        运行主程序
        """
        try:
            # 先测试网络连接
            if not self.test_connection():
                print("网络连接异常，请检查网络设置")
                return

            # 设置cookie
            if not self.set_cookies():
                print("设置cookie失败，程序退出")
                return

            # 获取所有教案链接
            blog_links = self.get_blog_links()
            if not blog_links:
                print("未找到任何教案链接")
                return

            print(f"找到 {len(blog_links)} 篇教案")

            # 循环访问每个教案
            while True:
                for link in blog_links:
                    self.view_blog(link)
                    # 在访问下一个教案前稍作停顿
                    time.sleep(random.uniform(2, 5))

        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            print(f"运行时出错: {e}")
        finally:
            self.driver.quit()


def main():
    viewer = BlogViewer()
    viewer.run()


if __name__ == "__main__":
    main()

