import jieba
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
#将csv换成txt


data = pd.read_csv('excel/exercisetopicdata.csv', encoding='utf-8')
with open('txt/exercisetopicdata.txt', 'w', encoding='utf-8') as f:
    for _, row in data.iterrows():
        f.write(row['Title'] + '\n' + row['Topics'] + '\n')
    f.close()


#导入电子书文本，并利用jieba进行分词
text=open("txt/exercisetopicdata.txt","r",encoding="utf-8").read()
words=jieba.lcut(text)

# 利用循环语句，进行词频统计 
#去除分词生成的单字
counts={}
for word in words:
    if len(word) == 1:
        continue

#非单字词语生成词频字典
#对分词进行词频统计、排序，并生成后续词云使用的词语列表
    else:
        counts[word]=counts.get(word,0)+1


#建立词云所用的词语列表
wordslist=""
items=list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
#遍历词频字典，并依据词频进行排序
cqlist=[]
for i in range(30):
    word,count=items[i]
    print("词:{}\t词频:{}".format(word,count))
    cqlist_=[word,count]
    cqlist.append(cqlist_)  
    wordslist=wordslist+word+" "
    # 创建DataFrame对象
df = pd.DataFrame(cqlist, columns=["词", "词频"])
# 导出为CSV文件
df.to_csv("excel/word.csv", index=False, encoding="utf-8")
#输出词频排名前200的词语及次数
#将词频排名前200的词语添加到词云列表中，并用空格进行间隔

#套用词云图形
mask=np.array(Image.open("pictures/bird.png"))

 #设置词云参数
pic=WordCloud(
    background_color="white",
    mask=mask,
    font_path="txt/AaJueXingHei65J.ttf",
    height=1200,
    width=1200).generate(wordslist)

 #从mask中提取颜色
from wordcloud import WordCloud,ImageColorGenerator
image_colors=ImageColorGenerator(mask)
plt.imshow(pic.recolor(color_func=image_colors))

#显示词云
plt.imshow(pic)
plt.axis("off")
plt.show()
#将词云图保存到文件
pic.to_file("pictures/exercisetopic.png")
