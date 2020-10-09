
from flask import Flask, render_template
import pandas as pd
import altair as alt

# 读取数据到内存
df = pd.read_excel("Data.xlsx")

# 生成图表
"""广州市各大租房网站不同户型的房源数量"""
df_alt = df.groupby("户型").size().sort_values(ascending = False).reset_index(name="房源数量")

bars = alt.Chart(df_alt).mark_bar().encode(
    y=alt.Y("房源数量"),
    x=alt.X("户型", sort = alt.EncodingSortField(field="房源数量",order="descending")),
)
text = bars.mark_text(
    align='center',
    baseline='middle',
    dy=-8  
).encode(
    text='房源数量'
)
alt.layer(bars, text).configure_view(
    stroke='transparent'
).configure_axis(
    domainWidth=0.8
)

chart1=(bars + text).properties(
    width=1000,
    height=900,
    title="广州市各大租房网站不同户型的房源数量"
)

"""广州市各区域户型种类数"""
df_alt1=df.groupby(['区域','户型']).size().reset_index()
df_alt2=df_alt1.groupby("区域").size().reset_index(name='户型种类')

bars = alt.Chart(df_alt2).mark_bar().encode(
    y=alt.Y("户型种类"),
    x=alt.X("区域", sort = alt.EncodingSortField(field="户型种类",order="descending")),
)
text = bars.mark_text(
    align='center',
    baseline='middle',
    dy=-8  
).encode(
    text='户型种类'
)
chart2 =(bars + text).properties(
    width=500,
    title="广州市各区域户型种类数"
)




"""不同区域不同户型的房源数量"""
df_alt3 = df.groupby(["区域", "户型"]).size().reset_index(name='房源数量')
input_dropdown = alt.binding_select(options=['从化区','南沙区','南海区','增城区','天河区','广州周边','海珠区','番禺区','白云区','花都区','荔湾区','越秀区','黄埔区'])
selection = alt.selection_single(fields=['区域'], bind=input_dropdown, name='district')
color = alt.condition(selection,
                    alt.Color('户型:N', legend=None),  
                    alt.value('lightgray'))
chart3 = alt.Chart(df_alt3).mark_bar().encode(
    x=alt.X("户型", sort = alt.EncodingSortField(field="房源数量",order="descending")),
    y=alt.Y("房源数量"),
    color='区域:N',
    tooltip='房源数量:N'    
).properties(
    height=400,
    title='不同区域不同户型的房源数量'
).add_selection(
    selection
).transform_filter(
    selection
)


"""使用面积与租金的关系"""
alt.data_transformers.disable_max_rows()
chart4=alt.Chart(df).mark_point(color='orange').encode(
    y='租金',
    x="使用面积"
).properties(
    width=1000,
    height=500,
    title='使用面积与租金的关系'
    ).interactive()

"""户型与租金的关系"""
alt.data_transformers.disable_max_rows()
chart5=alt.Chart(df).mark_point(color='red').encode(
    y='租金',
    x="户型"
).properties(
    width=700, 
    height=300,
    title='户型与租金的关系'
    ).interactive()

"""有无电梯与租金的关系"""
df_alt4=df.dropna()
chart6=alt.Chart(df_alt4).mark_point(color='red').encode(
    y='租金',
    x="有无电梯"
).properties(
    width=400, 
    height=300,
    title='租金与有无电梯的关系'
    ).interactive()

    

# 生成HTML文件
# chart1.save("广州市各大租房网站不同户型的房源数量.html")
# chart2.save("广州市各区域户型种类数.html")
# chart3.save("不同区域不同户型的房源数量.html")
chart4.save("使用面积与租金的关系.html")
# chart5.save("户型与租金的关系.html")
# chart6.save("租金与有无电梯的关系.html")