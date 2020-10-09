
import pandas as pd
import altair as alt

# 读取数据到内存
# df1 = pd.read_excel("朝向.xlsx")
# df2 = pd.read_excel("addresses.xlsx")


"""不同朝向的出租房价格"""
# scales = alt.selection_interval(bind='scales')

# chart = alt.Chart(df1).mark_point().encode(
#     x='朝向',
#     y='租金',
#     # color='Origin:N'
# ).properties(
#     width=700, 
#     height=500,
#     title='不同朝向的出租房价格'
# ).add_selection(
#     scales
# )


"""不同区域出租房数量"""
# df_alt = df2.groupby("area").size().reset_index(name='出租房数量')

# chart = alt.Chart(df_alt).mark_bar(color='orange').transform_fold(
#     fold=['出租房数量'], 
#     as_=['variable', 'value']
# ).encode(
#     x="area",
#     y="出租房数量",
#     color='variable:N'
# ).properties(
#     width=700, 
#     height=500,
#     title='不同区域的出租房数量'
#     )




"""区域、小区、出租房数量关系""" 
# df_alt1 = df2.groupby(["area", "小区"]).size().reset_index(name='小区数量')
# input_dropdown = alt.binding_select(options=['从化','南沙','南海','增城','天河','广州周边','海珠','番禺','白云','花都','荔湾','越秀','黄埔'])
# selection = alt.selection_single(fields=['area'], bind=input_dropdown, name='xiaoqu_of')
# color = alt.condition(selection,
#                     alt.Color('小区:N', legend=None),  
#                     alt.value('lightgray'))

# chart = alt.Chart(df_alt1).mark_point().encode(
#     x='小区',
#     y='小区数量',
#     color='area:N',
#     tooltip='小区:N'    
# ).properties(
#     height=400,
#     title='不同区域有房出租的小区的出租房数量'
# ).add_selection(
#     selection
# ).transform_filter(
#     selection
# )


# 生成HTML文件
# chart.save("不同朝向的出租房价格.html")
# chart.save("不同区域出租房数量.html")
# chart.save("区域、小区、出租房数量关系.html")
