from snownlp import SnowNLP
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

df = pd.read_csv('excel/exercisetopicdata2.csv',encoding='utf-8')
data = df[['Title', 'Topics','Stitle']]

# 创建新的DataFrame来存储情感分析结果
result_df = pd.DataFrame(columns=['Title', 'Topic1','Stitle','Sentiment'])

# 情感分析
for i in range(len(data)):
    row = data.iloc[i]
    sentiment_scores = []
    for topic in row:
        sentiment_scores.append(SnowNLP(topic).sentiments)
    result_df.loc[i] = [*row, np.mean(sentiment_scores)]

# 将情感分析结果写入CSV文件
result_df.to_csv('excel/exerciseemotion.csv', index=False, encoding='utf-8-sig')

# 统计情感分析结果
print(result_df.describe())

