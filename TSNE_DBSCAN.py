import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

######################################
embedding_vector = pd.read_json('./data/embeddings_64.json').T

tsne = TSNE(n_components=2, perplexity=20)
tsne_data = tsne.fit_transform(embedding_vector)

plt.figure()
plt.scatter(tsne_data[:, 0], tsne_data[:, 1])
plt.show()

# 数据预处理
scaler = StandardScaler()
scaled_data = scaler.fit_transform(tsne_data)

# 构建模型
# def select_MinPts(data,k):
#     k_dist = []
#     for i in range(data.shape[0]):
#         dist = (((data[i] - data)**2).sum(axis=1)**0.5)
#         dist.sort()
#         k_dist.append(dist[k])
#     return np.array(k_dist)
# k = 3  # 此处k取 2*2 -1 
# k_dist = select_MinPts(tsne_data,k)
# k_dist.sort()
# plt.figure()
# plt.plot(np.arange(k_dist.shape[0]),k_dist[::-1])


######################################
dbscan = DBSCAN(eps=3, min_samples=4)
# 模型拟合
dbscan.fit(tsne_data)

# 获取每个数据点的类别标签
labels = dbscan.labels_
plt.figure()

# 绘制经过预处理并使用 DBSCAN 聚类后的散点图，并根据类别标签设置颜色
plt.scatter(tsne_data[:, 0], tsne_data[:, 1], c=labels)
plt.show()
######################################

Area = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海",
        "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
        "广西", "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "宁夏", "新疆"]

Department = ["农林牧渔水利", "煤炭采选", "石油天然气开采", "黑色金属采选", "非金属矿产采选", "食品加工",
              "纺织工业", "服装及其他纤维制品", "木材加工, 竹, 甘蔗, 棕榈纤维及草制品", "造纸及纸制品",
              "石油加工及焦化", "化工原料及化工产品", "非金属矿产品", "黑色金属冶炼及压延", "金属制品",
              "普通机械", "特殊用途设备", "交通运输设备", "电气设备与机械", "电子通讯设备", "仪器仪表,文化办公机械",
              "其他制造业", "电力,蒸汽,热水生产与供应", "燃气生产与供应", "自来水生产与供应", "建筑",
              "运输, 存储年龄,邮电服务", "批发,零售贸易和餐饮服务"]


def Process(matrix):
    index_list = []
    column_list = []
    for i in matrix.index:
        index = Department[(i + 1) % 28 - 1]
        index_list.append(index)
    for j in matrix.columns:
        column = Department[(j + 1) % 28 - 1]
        column_list.append(column)

    matrix.index = index_list
    matrix.columns = column_list

    return matrix


def plot_flow(matrix):
    node_list = []
    edge_out_list = []
    edge_in_list = []

    node_list = [{"name": node} for node in matrix.index]

    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            edge = {
                "source": matrix.index[i],
                "target": matrix.columns[j],
                "value": matrix.iloc[i, j],
                "lineStyle": {"width": matrix.iloc[i, j]}
            }
            edge_out_list.append(edge)

    for i in range(matrix.shape[0]):
        for j in range(0, i):
            edge = {"source": matrix.index[i],
                    "target": matrix.columns[j],
                    "value": matrix.iloc[i, j],
                    "lineStyle": {"width": matrix.iloc[i, j]}
                    }
            edge_in_list.append(edge)

    graph = (
        Graph(init_opts=opts.InitOpts(width="1500px", height="800px"))
        .add("outflow",
             node_list, edge_out_list,
             repulsion=8000,
             linestyle_opts=opts.LineStyleOpts(curve=0.2),
             itemstyle_opts=opts.ItemStyleOpts(color="green")
             )
        .add("inflow",
             node_list, edge_in_list,
             repulsion=8000,
             linestyle_opts=opts.LineStyleOpts(curve=0.2),
             itemstyle_opts=opts.ItemStyleOpts(color="red")
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="类内碳转移图"))
        .render("./visualization/graph_chart.html")
    )


def plot_cluster_carbon_flow(label, matrix, tsne_data):
    province_labels = pd.DataFrame(index=embedding_vector.index)
    province_labels['label'] = labels

    #拼接聚类结果和对应的省份数据
    for i in province_labels.index:
        province_labels.loc[i, 'Area'] = Area[math.ceil((i + 1) / 28) - 1]
        province_labels.loc[i, 'Area_id'] = math.ceil((i + 1) / 28) - 1

    province_labels['x'] = tsne_data[:, 0]
    province_labels['y'] = tsne_data[:, 1]

    #筛选对应标签的碳转移矩阵
    label_data = province_labels[province_labels['label'] == label]
    filtered_index = province_labels[province_labels['label'] == label].index
    filtered_matrix = matrix.loc[filtered_index, filtered_index]

    filtered_matrix = Process(filtered_matrix)

    plt.figure()
    plt.scatter(label_data['x'], label_data['y'], c=label_data['Area_id'], label=f'Label {label}')
    plt.title(f'Scatter plot for Label {label}')
    plt.show()

    plot_flow(filtered_matrix)

    return filtered_matrix, province_labels


if __name__ == '__main__':
    matrix = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2012.json')
    filtered_matrix, province_labels = plot_cluster_carbon_flow(15, matrix, tsne_data)

######################################
'''
unique_labels = np.unique(labels)
for i in unique_labels:
    if(i!=-1):
        index=new_df[(new_df['label']==i)].index
        filtered_matrix = matrix_2012.loc[index, index]
        filtered_matrix = filtered_matrix.sort_index(axis=0).sort_index(axis=1)
        
        plt.figure()
        sns.heatmap(filtered_matrix, cmap="OrRd")

# unique_labels = set(labels)
# centers =[]
# for label in unique_labels:
#     if label != -1:
#         center =np.mean(X[labels= label],axis=0)
#         centers.append(center)
'''
