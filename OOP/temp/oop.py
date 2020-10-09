import pandas as pd
import altair as alt

df2=pd.read_excel('mianjiandjiage.xlsx')
df0=pd.read_excel('ziru.xlsx')

#广州各区租金与面积关系
areas=['请选择区域','荔湾区','白云区','海珠区','黄埔区','萝岗区','南沙区','从化区','花都区','番禺区','天河区','越秀区','增城区']
areas_dropdown = alt.binding_select(options=areas)
areas_select = alt.selection_single(fields=['区域'], bind=areas_dropdown,name="district")


mj=alt.Chart(df2).mark_bar().encode(
    x=alt.X("区域", sort=alt.EncodingSortField(field="平均使用面积/㎡")),
    y=alt.Y("平均使用面积/㎡"),
    color='平均使用面积/㎡'
)

mj2=alt.Chart(df2).mark_point(color="orange").encode(
    x=alt.X("区域", sort=alt.EncodingSortField(field="平均使用面积/㎡")),
    y=alt.Y("每月平均租金/元")
)

mj3=alt.Chart(df2).mark_text(color="red").encode(
    x=alt.X("区域", sort=alt.EncodingSortField(field="平均使用面积/㎡")),
    y=alt.Y("每月平均租金/元")
).add_selection(
    areas_select
).transform_filter(
    areas_select
)
#mark_text(align='left', dx=5)
zj=alt.Chart(df2).mark_line(color="orange").encode(
    x=alt.X("区域"),
    y=alt.Y("每月平均租金/元:Q", sort=alt.EncodingSortField(field="每月平均租金/元"))    
)

compound_graph3 = ( mj+zj+mj3).resolve_scale(y="independent").properties(width=700, height=300,title="广州各区租金与面积关系")


#compound_graph3


#地铁各线路房源数量与价格比照

new=df0.groupby('位置').size().sort_values(ascending=False).reset_index(name='房源数')
new2=df0.groupby('位置').apply(lambda x:x.groupby('价格').size().sort_values(ascending=False)).reset_index(name='none')

new3=new2.groupby('位置').apply(lambda x:x['价格'].mean()).round(decimals=0).reset_index(name='平均价格')

new4=df0.groupby('位置').apply(lambda x:x.groupby('线路').size().sort_values(ascending=False)).reset_index(name='线路1')

df_merge2=pd.merge(new3,new,on=['位置'],how='left')

df_merge3=pd.merge(df_merge2,new4,on=['位置'],how='left')

lines=['请选择线路','1号线','2号线','3号线','4号线','5号线','6号线','7号线','8号线','9号线','13号线','21号线','广佛线','APM线']
lines_dropdown = alt.binding_select(options=lines)
lines_select = alt.selection_single(fields=['线路'], bind=lines_dropdown,name="Lines")

curve1=alt.Chart(df_merge3).mark_bar().encode(
    alt.X("位置", sort=alt.SortField(field="房源数:N", order='descending')),
    alt.Y("房源数"),
    color='线路').add_selection(
    lines_select
).transform_filter(
    lines_select
)

curve2=alt.Chart(df_merge3).mark_line(color='red').encode(
  alt.X("位置"),
    alt.Y("平均价格:Q", sort=alt.SortField(field="平均价格")))
compound_graph = (curve1 + curve2).resolve_scale(y="independent").properties(width=3000,height=1000,title="地铁各线路房源数量与价格比照")

#compound_graph
