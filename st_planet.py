import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit.components.v1 as stc
import functions
import time

st.header("ケプラー方程式による惑星の会合計算")

# 楕円軌道の関数
def ellipse(i, a, e):
    u=np.pi/180*i
    b=a*np.sqrt(1-np.power(e,2))
    x=a*np.cos(u)-a*e
    y=b*np.sin(u)
    return x, y

# 日本標準時（JST）からユリウス暦（JD）への変換関数
def DAYtoJD(Year,Month,Day,Hour,Minute):
# 世界標準時（UT）を入力するので「-9」
#    DDay = Day+(Hour+Minute/60-9)/24
# ・・・・・
    return JD

# ユリウス暦（JD）から日本標準時（JST）への変換関数
def JDtoDAY(JD):
# JDはUTを変換したものなので，UT+9hのため9/24を加える
# ・・・・・
#    print('日本標準時（UT+9h）', Year, Month, Day, Hour, Minute)
    return Year, Month, Day, Hour, Minute


fig, ax = plt.subplots(dpi=100, figsize=(6, 6))
fig.patch.set_alpha(1.0)  # グラフの透明度
ax.set_xlim(-1.7, 1.3)
ax.set_ylim(-1.5, 1.5)

# 図中への文字列挿入位置設定
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

a = 1.0                                 # 楕円方程式のa
e = 0.3                                 # 楕円方程式のe
b = a * np.sqrt(1 - np.power(e,2))      # 楕円方程式のb
print('a,b,e=', a, b, e)

# 惑星軌道表示
tt = np.linspace(0, 2*np.pi, 180)       # 0～2πまでの範囲
phase = 0                               # 位相
x2 = a * np.cos(tt - phase) - a*e       # 1周期分の正弦波を作成
y2 = b * np.sin(tt - phase)

line, = ax.plot(x2, y2, label='ellipse', c='g', lw=1)

# 太陽，惑星の図中の初期位置設定
x3, y3 = ellipse(0, a, e)
sun, = ax.plot(0, 0, c='r', marker='o', markersize=10) # マーカー：unpackで,をつける
# marker, = ax.plot(0, 0, c='r', marker='o', markersize=8) # マーカー：unpackで,をつける
planet, = ax.plot(x3, y3, c='b', marker='o', markersize=8) # マーカー：unpackで,をつける

frames = 361 # フレーム数

the_plot = st.pyplot(plt)

def init():  # give a clean slate to start
    line.set_ydata([np.nan] * len(x2))

# アニメーション更新関数
def animate(frames_cnt):
    time_text.set_text('counts = %3d ' % (frames_cnt))
#    marker.set_ydata(np.sin(0 + 2*np.pi*(frames_cnt / frames))) # マーカーy座標更新
    xx3, yy3 = ellipse(frames_cnt, a, e)
    planet.set_xdata(xx3) # 惑星x座標更新
    planet.set_ydata(yy3) # 惑星y座標更新
    line.set_ydata(y2)
    the_plot.pyplot(plt)


col1, col2 = st.beta_columns(2)
with col1:
    start = st.button("start")
with col2:
    stop = st.button("stop")

save = []
if start:
    init()
    i = 0
    while True:
        i += 1
        animate(i)
        time.sleep(0.001)
        if stop:
            st.stop()


        
