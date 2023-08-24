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

# 读取 Excel 文件数据
df = pd.read_excel("excel/excercisetopicdata.xlsx")


# 将数据插入数据库
# 遍历数据行
for index, row in df.iterrows():
    try:
        # 从每一行获取对应的字段数据
        title = row['Title']
        topics_str = row['Topics']
        like = row['Likes']
        followers = row['Followers']
        views = row['Views']
        stitle = row['Stitle']

        # 将数据插入到 MySQL 数据库表中
        sql = "INSERT INTO data (title, topics, likes, followers, views, stitle) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (title, topics_str, like, followers, views, stitle))
        conn.commit()
    except Exception as e:
        print(f"插入数据时发生错误: {e}")
        continue

# 关闭数据库连接
conn.close()

print('所有数据已经保存完毕!')