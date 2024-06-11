import pandas as pd
import numpy as np
import json


def process_carbon_transfer(file_path, year):
    # 读取 JSON 文件
    matrix = pd.read_json(file_path)

    # 定义地区名称
    Area = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海",
            "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
            "广西", "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "宁夏", "新疆"]
    
    # 初始化空矩阵 30*30
    arr = np.zeros((len(Area), len(Area)))
    matrix_new = pd.DataFrame(arr, index=Area, columns=Area)

    # 读取原矩阵数据，对每行求和再保存到新矩阵30*30中
    for i in range(matrix.shape[0]):
        index = Area[i // 28]
        for j in range(matrix.shape[1]):
            column = Area[j // 28]
            matrix_new.loc[index, column] += matrix.iloc[i, j]


    # 将 DataFrame 转换为 JSON 格式，不包括索引和列名
    echarts_data = matrix_new.to_json(orient='values', index=False)

    # 保存为本地 JSON 文件
    output_file = f'./data/echarts_data_30*30_{year}.json'
    with open(output_file, 'w') as file:
        file.write(echarts_data)
        # json.dump(echarts_data, f) #这个会输出为字符串，带双引号的

    print(f'Data for {year} has been processed and saved to {output_file}')


if __name__ == '__main__':
    # 读取 JSON 文件 (省份*部门 * 省份*部门 = 840 * 840) => (总省份 * 总省份) 30 * 30
    process_carbon_transfer('./Sectors_Carbon_Transfer/sector_carbon_transfer_2017.json', 2017)
    process_carbon_transfer('./Sectors_Carbon_Transfer/sector_carbon_transfer_2015.json', 2015)
    process_carbon_transfer('./Sectors_Carbon_Transfer/sector_carbon_transfer_2012.json', 2012)
    