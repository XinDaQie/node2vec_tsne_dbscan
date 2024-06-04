import pandas as pd
import numpy as np
from tqdm import tqdm
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

Area = ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "上海市",
        "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省", "湖南省", "广东省",
        "广西壮族自治区", "海南省", "重庆市", "四川省", "贵州省", "云南省", "陕西省", "甘肃省", "青海省",
        "宁夏回族自治区", "新疆维吾尔自治区"]

carbon_data = pd.read_json('./data/province_2017.json')

outflow_list = []
inflow_list = []

np.fill_diagonal(carbon_data.values, 0)
row = carbon_data.sum(axis=1)
column = carbon_data.sum(axis=0)

row.index = Area
column.index = Area

min_outflow = min(row)
max_outflow = max(row)

min_inflow = min(column)
max_inflow = max(column)

for i in tqdm(range(carbon_data.shape[0])):
    for j in range(i + 1, carbon_data.shape[1]):
        outflow = (carbon_data.index[i], carbon_data.columns[j])
        outflow_list.append(outflow)

for i in tqdm(range(carbon_data.shape[0])):
    for j in range(0, i):
        inflow = (carbon_data.index[i], carbon_data.columns[j])
        inflow_list.append(inflow)

line = (
    Geo(init_opts=opts.InitOpts(width="1500px", height="1000px"))
    .add_schema(maptype="china")
    .add(
        "outflow",
        outflow_list,
        symbol_size=0.1,
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=2, color="green"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2, width=0.01, color="green"),
    )
    .add(
        "inflow",
        inflow_list,
        symbol_size=0.1,
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=2, color="red"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2, width=0.01, color="red"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines"))
    .render("./visualization/geo_lines.html")
)

carbon_outflow = (
    Map(init_opts=opts.InitOpts(width="1000px", height="800px"))
    .add("", [list(z) for z in zip(row.index, row)], "china", is_map_symbol_show=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="碳流出"),
        visualmap_opts=opts.VisualMapOpts(
            min_=0,
            max_=max_outflow,
            range_color=['#f6d2a9', '#f5b78e', '#f19c7c', '#ea8171', '#dd686c', '#ca5268', '#b13f64'],
            is_piecewise=True  # 是否分段显示
        )
    )
    .render("./visualization/carbon_outflow.html")
)

carbon_inflow = (
    Map(init_opts=opts.InitOpts(width="1000px", height="800px"))
    .add("", [list(z) for z in zip(column.index, column)], "china", is_map_symbol_show=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="碳流入"),
        visualmap_opts=opts.VisualMapOpts(
            min_=0,
            max_=max_inflow,
            range_color=['#c4e6c3', '#96d2a4', '#6dbc90', '#4da284', '#36877a', '#266b6e', '#1d4f60'],
            is_piecewise=True  # 是否分段显示
        )
    )
    .render("./visualization/carbon_inflow.html")
)
