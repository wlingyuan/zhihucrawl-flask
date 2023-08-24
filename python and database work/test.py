
from snownlp import SnowNLP
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
# 将情感分析结果写入CSV文件
result_df=pd.read_csv('excel/exerciseemotion.csv', index=False, encoding='utf-8-sig')
# 绘制情感分直方图
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.hist(result_df['Sentiment'], bins=np.arange(0, 1.1, 0.1), color='#4F94CD', alpha=0.9)
plt.xlim(0, 1)
plt.xlabel('情感分')
plt.ylabel('数量')
plt.title('情感分直方图')
plt.savefig('pictures/histogram', dpi=600)
plt.show()
# 绘制各情感占比
positive_count = len(result_df[result_df['Sentiment'] > 0.6])
negative_count = len(result_df[result_df['Sentiment'] < 0.4])
neutral_count = len(result_df[(result_df['Sentiment'] >= 0.4) & (result_df['Sentiment'] <= 0.6)])
print('积极评论数目为:', positive_count, '\n消极评论数目为:', negative_count)
pie_labels = 'positive', 'negative', 'neutral'
plt.pie([positive_count, negative_count,neutral_count], labels=pie_labels, autopct='%1.2f%%', shadow=0)
plt.title('情感占比图')
plt.savefig('pictures/pos&neg', dpi=600)
plt.show()