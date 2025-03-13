import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Open-Meteo APIのエンドポイントとパラメータ
API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 34.693738,  # 大阪の緯度
    "longitude": 135.502165,  # 大阪の経度
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
    "timezone": "Asia/Tokyo"
}

# 都市の選択
city = st.selectbox("都市を選択してください", ["東京", "大阪", "札幌", "福岡", "那覇", "名古屋", "仙台", "広島", "鹿児島"])

# 都市とその緯度・経度の辞書
city_coords = {
    "東京": (35.682839, 139.759455),
    "大阪": (34.693738, 135.502165),
    "札幌": (43.061936, 141.354292),
    "福岡": (33.590355, 130.401716),
    "那覇": (26.212401, 127.680932),
    "名古屋": (35.181446, 136.906398),
    "仙台": (38.268215, 140.869356),
    "広島": (34.385203, 132.455293),
    "鹿児島": (31.596553, 130.557115)
}

# 選択された都市に基づいて緯度と経度を設定
latitude, longitude = city_coords[city]

# APIリクエストのパラメータを更新
PARAMS.update({
    "latitude": latitude,
    "longitude": longitude
})

# APIリクエストを送信してデータを取得
response = requests.get(API_URL, params=PARAMS)
data = response.json()

# 天気コードを天気の状態に変換する関数
def weather_code_to_description(code):
    weather_dict = {
        0: "晴れ",
        1: "主に晴れ",
        2: "部分的に曇り",
        3: "曇り",
        45: "霧",
        48: "霧氷",
        51: "小雨",
        53: "雨",
        55: "大雨",
        56: "小雪",
        57: "雪",
        61: "小雨",
        63: "雨",
        65: "大雨",
        66: "小雪",
        67: "雪",
        71: "小雪",
        73: "雪",
        75: "大雪",
        77: "雪",
        80: "にわか雨",
        81: "にわか雨",
        82: "にわか雨",
        85: "にわか雪",
        86: "にわか雪",
        95: "雷雨",
        96: "雷雨",
        99: "雷雨"
    }
    return weather_dict.get(code, "不明")

# データをDataFrameに変換
daily_data = data['daily']
df = pd.DataFrame({
    "日付": daily_data['time'],
    "最高気温 (°C)": daily_data['temperature_2m_max'],
    "最低気温 (°C)": daily_data['temperature_2m_min'],
    "降水量 (mm)": daily_data['precipitation_sum'],
    "天気": [weather_code_to_description(code) for code in daily_data['weathercode']]
})

# Streamlitアプリの設定
st.title(f"{city}の1週間分の天気予報")
st.write(f"Open-MeteoのAPIを使用して取得した{city}の1週間分の天気予報です。")

# データフレームを表示
st.dataframe(df)

# 折れ線グラフを表示
line_fig = px.line(df, x="日付", y=["最高気温 (°C)", "最低気温 (°C)"], 
                   title="最高気温と最低気温の推移", labels={"value": "気温 (°C)", "variable": "凡例"})
st.plotly_chart(line_fig)

# 棒グラフを表示
bar_fig = px.bar(df, x="日付", y="降水量 (mm)", 
                 title="降水量の推移", labels={"降水量 (mm)": "降水量 (mm)"})
st.plotly_chart(bar_fig)