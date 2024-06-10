import streamlit as st
from datetime import datetime, timedelta
from api import get_data_from_sheet,append_to_sheet
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import altair as alt


# streamlit으로입력
# ● date
# ● type:식비,교통비,기타
# ● money
# ● 입력버튼
# 구글시트에내역저장
# ● 입력한내용이오른쪽과같이저장됨
# streamlit에서통계확인
# ● 주마다각종류의총액을꺾은선그래프로그려주기
# ● 대상:마지막입력의날짜로부터과거4주
# streamlit에날짜,type,금액을입력할칸이있다.9점==============================================
# streamlit에[입력]버튼이있다.2점============================================================
# date,type,금액을입력해두고입력버튼을누르면구글시트에입력이잘된다.15점==========================
# 날짜가streamlit의date_input으로구현되어있다.2점============================================
# 종류를dropdown으로선택하도록되어있다.2점===================================================
# 금액에숫자가아닌값이들어있는채로[입력]버튼을누르면warning을띄우고 구글시트에입력하지않고가만히있는다.5점
# 위문제를Exception을사용해서해결한다.5점
# 구글시트에서날짜,type,금액을읽어온다.15점============================================================
# 마지막입력의날짜로부터과거4주만읽어온다10점
# 읽어온값을streamlit에어떤형태로든보여준다.10점
# 읽어온값을오른쪽형태로보여준다.15점
# 소비가없는주,종류는0원으로처리한다.20점
# 요구사항에없지만추가로구현한유용한기능이있으면가산점최대10점

#现在累积的分数----45=15+15+9+2+2+2

#在谷歌表里面读取三个attribute，种类分为外变量，x轴为日期，y轴为金额，储存为panda dataframe。生成图
# 定义一个自定义异常类

#this is the division of getting variables from users
money = st.number_input(label="금액이 입력하세요",
                        step=1)
type = st.selectbox(label="종류를 선택하세요",
                      options=('교통','식비','기타'),
                      format_func=str)
date = st.date_input(label='날짜를 선택하세요')
min_date = date - timedelta(weeks=4)
#the input button division
if st.button('입력'):
    try:
        money = float(money)
        append_to_sheet(range_name='A:C', values=[str(date), type, money])
        st.success("정상적으로 처리됨！")
    except ValueError:
        st.error("Warning:금액은 반드시 숫자다!")

st.subheader('histogram of the consumption in last 4 weeks')
data = get_data_from_sheet('1vM2UylvCuIcBQrWf8p_xiGE0sNdpg1_XgwT2VOjrQIg', 'A:C')
df = pd.DataFrame(data)
df.columns = ['date', 'type', 'money']
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# datedf = pd.to_datetime(df['date'][1:]) 
# moneydf = df['money'][1:].astype(int) 
# typedf = df['type'][1:]




# st.line_chart(data=df,x=date,y=money)

plot_df = df.iloc[1:, :]  # 从第二行开始读取所有列

# 绘制图表
chart = alt.Chart(plot_df).mark_line().encode(
    x='date:T',
    y='money:Q'
).properties(
    width='container',  # 宽度自适应
    height=400          # 高度可以根据需要设置
).interactive()

# 在 Streamlit 中展示图表
st.altair_chart(chart, use_container_width=True)

st.dataframe(df)

#connect df to the session
if 'data' not in st.session_state:
    st.session_state.data = df

# 如果 DataFrame 为空，添加一个名为 'date' 的列
if st.session_state.data.empty:
    st.session_state.data['date'] = pd.to_datetime([])

# 获取最新日期的四周前的日期
last_date = st.session_state.data['date'].max()
four_weeks_ago = last_date - pd.Timedelta(weeks=4)

# 过滤最近四周的数据
recent_data = st.session_state.data.loc[st.session_state.data['date'].between(four_weeks_ago, last_date)]

# 如果 recent_data 为空，返回空的DataFrame
if recent_data.empty:
    st.write("最近四周的数据为空。")
else:
    # 按每周进行重新采样并求和
    weekly_data = recent_data.resample('W', on='date').sum()

    # 显示重新采样后的数据
    st.write("最近四周的数据：")
    st.write(weekly_data)