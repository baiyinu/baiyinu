# 导入selenium的浏览器驱动接口
from selenium import webdriver
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.firefox.options import Options

# 创建firefox浏览器驱动，无头模式（超爽）
firefox_options = Options()
firefox_options.set_headless()
driver = webdriver.Firefox(firefox_options=firefox_options)
# driver = webdriver.Firefox()
# 加载百度页面
driver.get("http://www.baidu.com/")
# time.sleep(3)
# 获取页面名为wrapper的id标签的文本内容
data = driver.find_element_by_id("wrapper").text
print(data)
# 打印页面标题 "百度一下，你就知道"
print(driver.title)
# 生成当前页面快照并保存
driver.save_screenshot("baidu.png")
# 关闭浏览器
driver.quit()
webdriver.