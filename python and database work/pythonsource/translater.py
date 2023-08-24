import pandas as pd

def csv_to_excel(csv_file_path, excel_file_path):
    # 读取CSV文件
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # 将数据保存为Excel文件
    df.to_excel(excel_file_path, index=False)
    
    print("转化完成")

# # 输入CSV文件路径和目标Excel文件路径
# csv_file_path = input("请输入CSV文件路径: ")
# excel_file_path = input("请输入Excel文件路径: ")

# # 调用函数进行转换
# csv_to_excel(csv_file_path, excel_file_path)


def excel_to_csv(excel_file_path, csv_file_path):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file_path)

    # 将数据保存为 CSV 文件
    df.to_csv(csv_file_path, index=False)

    print("转化完成")

# 输入 Excel 文件路径和目标 CSV 文件路径
excel_file_path = input("请输入 Excel 文件路径: ")
csv_file_path = input("请输入 CSV 文件路径: ")

# 调用函数进行转换
excel_to_csv(excel_file_path, csv_file_path)




