import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('株価可視化アプリ')

st.sidebar.write("""
# 日本特定株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""

## 表示日数選択
""")

days = st.sidebar.slider('日数(年間取引日数245日)', 1, 245, 20)

st.write(f"""
### 過去 **{days}日間** の株価
""")
         

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0, 1500, (400, 1200)
    )

    tickers = {
    '北陸電力': '9505.T',
    '日本製紙': '3863.T',
    'ほくほくフィナンシャルグループ': '8377.T'
}
    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択できます。',
        list(df.index),
        ['北陸電力','日本製紙','ほくほくフィナンシャルグループ']
    )

    if not companies:
        st.error('少なくとも1社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (JPN)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(JPN)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(JPN):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです。"
    )



st.write(f"""
### 過去 **{days}日間** の日経平均株価
""")

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## 日経平均株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        20000, 36000, (25000, 30000)
    )

    tickers = {
    '日経225': '^N225'
}
    df = get_data(days, tickers)
    companies = st.multiselect(
        '日経225が表示されます。',
        list(df.index),
        ['日経225']
    )

    if not companies:
        st.error('少なくとも1つは選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices:Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！なにかエラーが起きているようです。"
    )