import pandas as pd
import numpy as np
import json

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
for i in range(matrix_2017.shape[0]):
    index = Area[i // 28]
    for j in range(matrix_2017.shape[1]):
        column = Area[j // 28]
        provinces.loc[index, column] += matrix_2017.iloc[i, j]

# 将DataFrame转换为ECharts热力图所需的格式
heatmap_data = []
for i in range(provinces.shape[0]):
    for j in range(provinces.shape[1]):
        heatmap_data.append([i, j, provinces.iloc[i, j]])

# 计算行和列的和，用于边缘的柱状图
row_sum = np.sum(provinces, axis=1).tolist()
col_sum = np.sum(provinces, axis=0).tolist()

# 将数据保存为JSON格式
echarts_data = {
    "heatmap_data": heatmap_data,
    "row_sum": row_sum,
    "col_sum": col_sum,
    "areas": Area
}

with open('./data/echarts_data.json', 'w') as f:
    json.dump(echarts_data, f)
