import pandas as pd

# 读取Excel文件
df = pd.read_excel("excel/excercisetopicdata.xlsx")

# 删除Title字段内容重复的行数据，只保留第一个
df_duplicates_removed = df.drop_duplicates(subset='Title', keep='first')

# 将处理后的数据保存到新的Excel文件
df_duplicates_removed.to_excel("excel/excercisetopicdata_duplicates_removed.xlsx", index=False)

print("数据已保存到新的Excel文件。")
