import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # 热力图
from tqdm import tqdm  # 在迭代时显示进度条
import math
from matplotlib.gridspec import GridSpec

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams['axes.unicode_minus'] = False

# 使用pandas的read_json()方法读取JSON文件  
matrix_2012 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2012.json')
matrix_2015 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2015.json')
matrix_2017 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2017.json')

Area = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海",
        "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
        "广西", "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "宁夏", "新疆"]
arr = np.zeros((len(Area), len(Area)))
province = pd.DataFrame(arr, index=Area, columns=Area)

#
for i in tqdm(range(matrix_2017.shape[0])):
    index = Area[i // 28]
    for j in range(matrix_2017.shape[1]):
        column = Area[j // 28]
        province.loc[index, column] += matrix_2017.iloc[i, j]


province.to_excel("./data/province.xlsx")
# province=pd.DataFrame(arr)


def plot(province):
    # 创建画布和网格布局
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(12, 12, figure=fig, hspace=0, wspace=0)

    # 在网格布局中放置热力图
    ax_heatmap = fig.add_subplot(gs[:10, :10])
    sns.heatmap(province, cmap="OrRd", cbar=False, ax=ax_heatmap, linewidths=1)

    # 获取数据的行列和
    row_sum = np.sum(province, axis=1)
    col_sum = np.sum(province, axis=0)

    # 在网格布局中放置右边的水平柱状图
    ax_bar_right = fig.add_subplot(gs[:10, 10:])
    ax_bar_right.barh(np.arange(len(Area)), col_sum, color='lightcoral')
    ax_bar_right.invert_yaxis()
    ax_bar_right.yaxis.set_ticks_position('right')
    ax_bar_right.xaxis.set_visible(False)
    ax_bar_right.yaxis.set_visible(False)
    ax_bar_right.spines['top'].set_visible(False)
    ax_bar_right.spines['bottom'].set_visible(False)
    ax_bar_right.spines['left'].set_visible(False)
    ax_bar_right.spines['right'].set_visible(False)

    # 在网格布局中放置下边的竖直向下的柱状图
    ax_bar_bottom = fig.add_subplot(gs[10:, :10])
    ax_bar_bottom.bar(np.arange(len(Area)), -row_sum, color='lightseagreen', align='center')
    ax_bar_bottom.xaxis.set_ticks_position('bottom')
    ax_bar_bottom.yaxis.set_visible(False)
    ax_bar_bottom.xaxis.set_visible(False)
    ax_bar_bottom.spines['top'].set_visible(False)
    ax_bar_bottom.spines['bottom'].set_visible(False)
    ax_bar_bottom.spines['left'].set_visible(False)
    ax_bar_bottom.spines['right'].set_visible(False)

    # 调整柱状图和热力图之间的间距
    for ax in [ax_bar_right, ax_bar_bottom]:
        ax.margins(0)
        for spine in ax.spines.values():
            spine.set_edgecolor('none')

    plt.show()


plot(province)
