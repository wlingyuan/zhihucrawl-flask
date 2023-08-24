import re
import jieba.posseg as psg
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

filtered_df=pd.read_csv('excel/exercisetopicdata.csv', encoding='utf-8')
def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword
def chinese_word_cut(mytext):
    words = open("txt/stopwords.txt", "r", encoding="utf-8")
    excludes = words.read().split("\n")
    ls2=psg.lcut(mytext)
    flag_list = ['n','nz','vn']
    word_list = []
    for list in ls2:
        word = re.sub(u'[^\u4e00-\u9fa5]','',list.word)
        #word =list.word  #如果想要分析英语文本，注释这行代码，启动下行代码
        find = 0
        for stop_word in excludes:
            if stop_word == word or len(word)<2:     #this word is stopword
                find = 1
                break
            if find == 0 and list.flag in flag_list:
                word_list.append(word)  
    return" ".join(word_list)
filtered_df["content_cutted"] = filtered_df.Title.apply(chinese_word_cut)
n_features = 1000
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',\
                                    max_features=n_features,\
                                    stop_words='english',\
                                    max_df = 0.5,\
                                    min_df = 2)
print(tf_vectorizer)
tf = tf_vectorizer.fit_transform(filtered_df.content_cutted)    
print(tf)
n_topics = 8  #主题数量需要认为定义
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,\
                                    learning_method='batch',\
                                    learning_offset=50,\
                                    # doc_topic_prior=0.1, #alpha参数，可以不定义\
                                    # topic_word_prior=0.01, #beta参数，可以不定义\
                                random_state=0)
lda.fit(tf)
# 2.1输出每个主题对应的词语的概率分布 
n_top_words = 25
tf_feature_names = tf_vectorizer.get_feature_names()
topic_word = print_top_words(lda, tf_feature_names, n_top_words)
# 2.2输出每篇文章对应主题的概率分布 
import numpy as np
topics=lda.transform(tf)
topic = []
for t in topics:
    topic.append("Topic #"+str(list(t).index(np.max(t))))
filtered_df['概率最大的主题序号']=topic
filtered_df['每个主题对应概率']=list(topics)
filtered_df.to_excel("topics.xlsx",index=False)
# 2.3可视化主题 
pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
#pyLDAvis.display(pic)
# pyLDAvis.save_html(pic, 'lda_pass'+str(n_topics)+'.html')  #保存html文档会使程序运行很慢，可以不用保存
pyLDAvis.display(pic)
#去工作路径下找保存好的html文件
#和视频里讲的不一样，目前这个代码不需要手动中断运行，可以快速出结果
#2.4计算困惑度：用于判断最佳主题个数，也可以用主题相似度来确定 
plexs = []
scores = []
n_max_topics = 16
for i in range(1,n_max_topics):
    print(i)
    lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                        learning_method='batch',
                                        learning_offset=50,random_state=0)
    lda.fit(tf)
    plexs.append(lda.perplexity(tf))
    scores.append(lda.score(tf))
n_t=15#区间最右侧的值。注意：不能大于n_max_topics
x=list(range(1,n_t+1))
plt.plot(x,plexs[0:n_t])
plt.xlabel("number of topics")
plt.ylabel("perplexity")
plt.savefig('pictures/perplexity_plot.png')
plt.show()
print("分析结束!")