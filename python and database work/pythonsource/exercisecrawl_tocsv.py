import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pymysql

# Establish a connection to MySQL database
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='wxc20021212',
    db='',
    charset='utf8'
)
cur = conn.cursor()

urllist = []  # 创建一个空列表用于存储网址

with open('excel/zhihutitlelink.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        url = row['标题链接']  # 获取每行的'标题链接'字段的值
        urllist.append(url)  # 将网址添加到列表中

# 打印输出网址列表
print(urllist)
print(len(urllist))

datalist = []  # 创建一个空列表用于存储数据

for i in range(120):
    url = urllist[i]
    try:
        driver = webdriver.Edge()
        driver.get(url)
        time.sleep(3)
        html = driver.page_source

        # 点掉知乎的登录弹窗
        button2 = driver.find_elements_by_xpath("""//button[@aria-label = '关闭']""")[0]
        button2.click()

        # 大标题
        wait = WebDriverWait(driver, 10)
        tit = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/h1')))
        title = tit.text
        
        # 小标题
        wait = WebDriverWait(driver, 10)
        button2= driver.find_element_by_class_name("Button.QuestionRichText-more.Button--plain")
        button2.click()
        Stitle_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="RichText ztext css-1g0fqss"]')))
        Stitle = Stitle_element.text

        # 主题
        topiclist = []
        topics = driver.find_elements_by_xpath('//a[@class="TopicLink"]/div')
        for topic in topics:
            topiclist.append(topic.text)
        
        # 点赞数
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[2]/div/div/div[2]/div[1]/button')))
        like = element.text.split()[-1]

        # 评论数和浏览量
        elements = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[2]')
        numbers = elements.text.split('被浏览')
        followers = numbers[0].strip('关注者\n').replace(',', '')
        views = numbers[1].strip('\n').replace(',', '')

        # 将主题列表转换为字符串
        topics_str = ', '.join(topiclist)

        # 将数据添加到数据列表
        urldata = [title, topics_str, like, followers, views]
        print(urldata)
        datalist.append(urldata)
        print('数据已保存完毕！')

        # 将数据插入到 MySQL 数据库表中
        # sql = "INSERT INTO data (title, topics, likes, followers, views) VALUES (%s, %s, %s, %s, %s)"
        # cur.execute(sql, (title, topics_str, like, followers, views))
        # conn.commit()
        # print('数据已经存入数据库!')
  
    except Exception as e:
        print(f'爬取网址 {url} 发生异常：{str(e)}')
        driver.quit()
    continue

# 创建数据框
columns = ['Title', 'Topics', 'Likes', 'Followers', 'Views']
df = pd.DataFrame(datalist, columns=columns)

# 保存为 CSV 文件（使用UTF-8编码）
df.to_csv('excel/excercisetopicdata.csv', index=False, encoding='utf-8')
print('所有数据已经保存完毕!')











