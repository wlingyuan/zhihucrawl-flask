#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time     : 2023/6/29 23:13
# @Author   :  DingJun
# @File     : LDA.py
import pyLDAvis.sklearn
import xlwt
import pyLDAvis
import numpy as np
from pyecharts.charts import Line
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
import jieba
import re
import os
from pyecharts import options as opts

data = pd.read_excel('excel/exercisetopicdata.xlsx')
data['text'] = data['Title']
data.drop(columns=['Title', 'Stitle'], inplace=True)

print("=========================合并列后的data==============================")
print(list(data.columns))
print(data)
stop_words = [line.strip() for line in open('./txt/stopwords.txt', 'r', encoding='utf-8').readlines()]

# 去重、去缺失、分词
pattern = u'[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!\t"@#$%^&*\\-_=+，。\n《》、？：；“”‘’｛｝【】（）…￥！—┄－]+'
data['cut'] = (
    data['text']
        .apply(lambda x: str(x))
        .apply(lambda x: re.sub(pattern, ' ', x))
        .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in stop_words]))
)


def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword


# 构造 TF-IDF
n_features = 1000
tf_idf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english',
                                    max_df=0.5,
                                    min_df=2)
tf_idf = tf_idf_vectorizer.fit_transform(data['cut'])
# 特征词列表
feature_names = tf_idf_vectorizer.get_feature_names()
# 特征词 TF-IDF 矩阵
matrix = tf_idf.toarray()
feature_names_df = pd.DataFrame(matrix, columns=feature_names)
print("========================词频矩阵输出=========================")
print(feature_names_df)

n_topics = 8 # 主题数量
# lda模型
lda = LatentDirichletAllocation(
    n_components=n_topics,
    max_iter=50,
    learning_method='batch',
    learning_offset=50,
    random_state=0)

# 使用 tf_idf 语料训练 lda 模型
res_lda = lda.fit(tf_idf)
print("===================使用 tf_idf 语料训练 lda 模型==============")
n_top_words = 20  # 输出每个主题对应的词语的概率分布
topic_word = print_top_words(lda, feature_names, n_top_words)

topics = lda.transform(tf_idf)
topic = []
for t in lda.transform(tf_idf):
    topic.append("Topic" + str(list(t).index(np.max(t))))

data['每个主题的概率'] = list(topics)
data['最有可能的主题'] = topic
data.to_excel("excel/topic.xlsx", index=False)

# 2.4计算困惑度：用于判断最佳主题个数，也可以用主题相似度来确定,一般主题数越多困惑度越低
plexs = []
scores = []
n_max_topics = 16
for i in range(1, n_max_topics):
    lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50, random_state=0)
    lda.fit(tf_idf)
    plexs.append(lda.perplexity(tf_idf))
    scores.append(lda.score(tf_idf))
plexs.reverse()
n = 15  # 区间最右侧的值。注意：不能大于n_max_topics
x = list(range(1, n + 1))


def get_line():
    line = (
        Line()
            .add_xaxis(xaxis_data=x)
            .add_yaxis(
            series_name="LDA主题分析",
            y_axis=plexs[0:n],
            is_symbol_show=False
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="LDA主题分析图"),
                             xaxis_opts=opts.AxisOpts(type_="category", name="number of topics",
                                                      name_location='center',
                                                      name_gap=30,
                                                      is_show=True),
                             yaxis_opts=opts.AxisOpts(
                                 type_="value",
                                 name="perplexity",
                                 name_location='center',
                                 name_rotate=90,
                                 name_gap=30,
                                 axistick_opts=opts.AxisTickOpts(is_show=True),
                                 splitline_opts=opts.SplitLineOpts(is_show=True),
                             ),
                             )
            .render('LDA主题分析图.html')
    )


get_line()

html_path = '../file/document-lda-visualization.html'
try:
    data = pyLDAvis.sklearn.prepare(lda, tf_idf, tf_idf_vectorizer)
    pyLDAvis.save_html(data, html_path)
    # 清屏
    os.system('clear')
    # 浏览器打开 html 文件以查看可视化结果
    os.system(f'start {html_path}')
except Exception as e:
    print("warnings")
print('本次生成了文件：', html_path)
