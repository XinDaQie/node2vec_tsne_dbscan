import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE


######################################
embedding_vector = pd.read_json('./data/embeddings_test.json').T

tsne = TSNE(n_components=2, perplexity=20)
tsne_data = tsne.fit_transform(embedding_vector)

plt.figure()
plt.scatter(tsne_data[:, 0], tsne_data[:, 1])
plt.show()


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

matrix_2012 = pd.read_json('./Sectors_Carbon_Transfer/sector_carbon_transfer_2012.json')

Area = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海",
        "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东",
        "广西", "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "宁夏", "新疆"]

new_df = pd.DataFrame(index=embedding_vector.index)
new_df['label'] = labels

for i in new_df.index:
    new_df.loc[i, 'Area'] = Area[math.ceil(i / 28) - 1]

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
'''

# unique_labels = set(labels)
# centers =[]
# for label in unique_labels:
#     if label != -1:
#         center =np.mean(X[labels= label],axis=0)
#         centers.append(center)

