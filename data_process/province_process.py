import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # 热力图
from tqdm import tqdm  # 在迭代时显示进度条
from matplotlib.gridspec import GridSpec

plt.rcParams["font.sans-serif"] = ["STHeiti"]
plt.rcParams['axes.unicode_minus'] = False

# 使用pandas的read_json()方法读取JSON文件  
matrix_2012 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2012.json')
matrix_2015 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2015.json')
matrix_2017 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2017.json')

Area = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海",
        "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
        "广西", "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "宁夏", "新疆"]
arr = np.zeros((len(Area), len(Area)))
provinces = pd.DataFrame(arr, index=Area, columns=Area)

# 读取数据
for i in tqdm(range(matrix_2017.shape[0])):
    index = Area[i // 28]
    for j in range(matrix_2017.shape[1]):
        column = Area[j // 28]
        provinces.loc[index, column] += matrix_2017.iloc[i, j]

provinces.to_excel("./data/province_2017.xlsx")

