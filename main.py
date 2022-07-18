from inspect import Parameter
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import functions as func
import time
from PIL import Image

st.set_page_config(page_title="会合シミュレーション")

page_id = 1

col1, col2 = st.columns(2)
with col1:
    if st.button("シミュレーションへ"):
        page_id = 1
with col2:
    if st.button("説明を見る"):
        page_id = 2

def simulation_page():
    st.header("地球と火星の会合シミュレーション")
    st.write('<p>地球と火星の会合周期からシミューションを動かします。</p><p>地球と火星の会合が観測された2018年7月31日を開始時刻とし、次に会合が観測された2020年10月6日を終了時刻としています。</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    # --------------------初期設定値------------------------


    # 開始・終了時刻設定
    Year1 = 2018
    Month1 = 7
    Day1 = 31
    Hour1 = 0
    Minute1 = 0
    JD1 = func.DayToJD(Year1,Month1,Day1,Hour1,Minute1)

    Year2 = 2020
    Month2 = 10
    Day2 = 6
    Hour2 = 0
    Minute2 = 0
    JD2 = func.DayToJD(Year2,Month2,Day2,Hour2,Minute2)

    # 時刻の表示文字
    YMD1 = '開始時刻: ' + str(Year1) + '.' + str(Month1) + '.' + str(Day1)
    YMD2 = '終了時刻: ' + str(Year2) + '.' + str(Month2) + '.' + str(Day2)

    with col3:
        st.write(YMD1)
        st.write(YMD2)


    # --------------------惑星のパラメータ------------------------


    # ~地球のパラメータ~
    class Earth:
        a = 1.00000102 # 軌道半長径a（天文単位）
        e = 0.01671022 # 離心率e
        ohm = np.pi/180* 174.838 # 昇交点黄経Ω（°→rad）
        i = np.pi/180* 0.002 # 軌道傾斜角i（°→rad）
        omega = np.pi/180*(102.972 - 174.838) # ω = (近日点黄経 - 昇交点黄経)
        T = 365.24 # 公転周期 (日)
        b = a*np.sqrt(1-np.power(e,2)) # 軌道半短径b（天文単位）
        n = 2*np.pi/T # 平均運動

        # 三角関数の値
        cosohm = np.cos(ohm) # 昇交点黄経Ωのcos
        sinohm = np.sin(ohm) # 昇交点黄経Ωのsin
        cosi = np.cos(i) # 軌道傾斜角iのcos
        sini = np.sin(i) # 軌道傾斜角iのsin
        cosomega = np.cos(omega) # ω = (近日点黄経 - 昇交点黄経)のcos
        sinomega = np.sin(omega) # ω = (近日点黄経 - 昇交点黄経)のsin

        # 地球近日点　2010/01/03 9:09:00 2455199.50625　国立天文台HP
        t0 = 2455199.50625

        # 長軸
        ax1,ay1,az1 = func.coordinate_transformation(-2.5,0,cosohm,sinohm,cosi,sini,cosomega,sinomega)
        ax2,ay2,az2 = func.coordinate_transformation(2.5, 0,cosohm,sinohm,cosi,sini,cosomega,sinomega)

        # 地球軌道表示
        t = np.linspace(0, 2*np.pi, 180)       # 0～2πまでの範囲
        phase = 0                               # 位相
        xx = a * np.cos(t - phase) - a*e       # 1周期分の正弦波を作成
        yy = b * np.sin(t - phase)
        x, y, z = func.coordinate_transformation(xx,yy,cosohm,sinohm,cosi,sini,cosomega,sinomega)

    # ~火星のパラメータ~
    class Mars:
        a = 1.52371034 # 起動半長径a（天文単位）
        e = 0.09339410 # 離心率e
        ohm = np.pi/180* 49.6198 # 昇交点黄経Ω（°→rad）
        i = np.pi/180* 1.8497 # 起動傾斜角i（°→rad）
        omega = np.pi/180*(336.2075 - 49.6198)
        T = 686.98 # 公転周期（日）
        b = a*np.sqrt(1-np.power(e,2)) # 軌道半短径b（天文単位）
        n=2*np.pi/T # 平均運動

        # 三角関数の値
        cosohm = np.cos(ohm)
        sinohm = np.sin(ohm)
        cosi = np.cos(i)
        sini = np.sin(i)
        cosomega = np.cos(omega)
        sinomega = np.sin(omega)
        # 火星近日点　2009/04/21 18:46:00 2454942.90694　国立天文台HP
        t0 = 2454942.90694

        # 長軸
        ax1,ay1,az1 = func.coordinate_transformation(-2.5,0,cosohm,sinohm,cosi,sini,cosomega,sinomega)
        ax2,ay2,az2 = func.coordinate_transformation(2.5, 0,cosohm,sinohm,cosi,sini,cosomega,sinomega)

        # 火星軌道表示
        t = np.linspace(0, 2*np.pi, 180)       # 0～2πまでの範囲
        phase = 0                               # 位相
        xx = a * np.cos(t - phase) - a*e       # 1周期分の正弦波を作成
        yy = b * np.sin(t - phase)
        x, y, z = func.coordinate_transformation(xx,yy,cosohm,sinohm,cosi,sini,cosomega,sinomega)


    # --------------------matplotlibの設定------------------------


    fig, ax = plt.subplots(dpi=100, figsize=(6, 6))
    fig.patch.set_alpha(1.0)  # グラフの透明度
    ax.set_xlim(-2.1, 1.9)
    ax.set_ylim(-2.0, 2.0)
    ax.grid()

    fdic = {
        "family" : "Georgia",
        "style" : "italic",
        "size" : 15,
        "color" : "black"
    }

    # 座標軸
    ax.text(1.7, -0.2, 'X', fontdict = fdic)
    ax.text(1.5, 0.2, 'Vernal', fontdict = fdic)
    ax.text(1.5, 0.05, 'equinox', fontdict = fdic)
    ax.text(-0.2, 1.8, 'Y', fontdict = fdic)

    # 地球の長軸の描画
    ax.plot([Earth.ax1, Earth.ax2],[Earth.ay1,Earth.ay2], color="blue", linestyle='dashdot', lw=0.7)
    ax.text(-1.1, 1.75, 'Earth-x', fontdict = fdic)

    # 火星の長軸の描画
    ax.plot([Mars.ax1, Mars.ax2],[Mars.ay1, Mars.ay2], color="blue", linestyle='dashdot', lw=0.7)
    ax.text(1.5, -1.0, 'Mars-x', fontdict = fdic)

    ax.plot(Mars.x, Mars.y, label='ellipse Marse', c='g', lw=1)

    # 図中への文字列挿入位置設定
    time_text = ax.text(-2.0, 1.85, '')
    JD_text = ax.text(-2.0, -1.8, '')
    UT9h_text = ax.text(-2.0, -1.95, '')


    # --------------------アニメーションの設定------------------------


    # フレーム数
    frames = int(JD2 - JD1) + 1

    the_plot = st.pyplot(plt)

    lineE, = ax.plot(Earth.xx, Earth.yy, label='ellipse Earth', c='g', lw=1)


    # アニメーション更新関数
    @st.cache
    def animate(frames_cnt, stop_animation):
        if stop_animation:
            print('stop!!')
        else:
            JD = JD1 + frames_cnt
            tt = JD
            JD_text.set_text('JD(UT): %7d ' % (JD))
            Year, Month, Day, Hour, Minute = func.JDToDay(JD)
            UT9h_text.set_text('UT+9h: %d.%d.%d' % (Year, Month, Day))
            time_text.set_text('counts = %3d ' % (frames_cnt))

            # 惑星の離心近点角　ケプラー方程式を解く
            # 地球
            uE0 = Earth.n*(tt-Earth.t0)
            uE1 = uE0
            for nnE in range(5):
                uE2 = uE1-func.Kepller_function(Earth.n, tt, Earth.t0, Earth.e, uE1)/func.diff_function(Earth.e, uE1)
                DIFE = uE2-uE1
                uE1 = uE2   
            xxE, yyE = func.ellipse_Kepller(uE1, Earth.a, Earth.e)
            x_E, y_E, z_E = func.coordinate_transformation(xxE,yyE, Earth.cosohm,Earth.sinohm,Earth.cosi,Earth.sini, Earth.cosomega, Earth.sinomega)
            planetE.set_xdata(x_E) # 地球x座標更新
            planetE.set_ydata(y_E) # 地球y座標更新
            lineE.set_ydata(Earth.yy)

            # 火星
            uM0 = Mars.n*(tt-Mars.t0)
            uM1 = uM0
            for nnM in range(10):
                uM2 = uM1-func.Kepller_function(Mars.n, tt, Mars.t0, Mars.e, uM1)/func.diff_function(Mars.e, uM1)
                DIFE = uM2-uM1
                uM1 = uM2   
            xxM, yyM = func.ellipse_Kepller(uM1, Mars.a, Mars.e)
            x_M, y_M, zM = func.coordinate_transformation(xxM, yyM, Mars.cosohm,Mars.sinohm,Mars.cosi,Mars.sini, Mars.cosomega, Mars.sinomega)
            planetM.set_xdata(x_M) # 火星x座標更新
            planetM.set_ydata(y_M) # 火星y座標更新

            the_plot.pyplot(fig)

    # streamlitの設定

    # st.sidebar.markdown("## Settings")

    speed = st.slider("惑星の速度", 1, 10)

    col1, col2 = st.columns(2)
    with col1:
        start = st.button("start")
    with col2:
        stop = st.button("stop")

    save = []
    if start:
        # 太陽，地球，火星の図中の初期位置設定

        # 地球の位置
        xE, yE = func.calc_coordinates(0, Earth.a, Earth.e)
        planetE, = ax.plot(xE, yE, c='blue', marker='o', markersize=10) 

        # 火星の位置
        xM, yM = func.calc_coordinates(0, Mars.a, Mars.e)
        planetM, = ax.plot(xM, yM, c='brown', marker='o', markersize=8) 

        # 太陽の位置
        sun, = ax.plot(0, 0, c='red', marker='o', markersize=14) # マーカー：unpackで,をつける

        i = 0
        stop_animation = False
        while True:
            animate(i, stop_animation)
            if (frames-speed) <= i:
                i = frames
                animate(i, stop_animation)
                st.stop()
            elif stop:
                stop_animation = True
            else:
                # 惑星の速度
                i += speed


# -------------------- 説明ページ --------------------
def explanation_page():
    st.title("地球と火星の会合計算")
    # 1. 地球と火星の会合周期
    r'''
    ### 1. 地球と火星の会合周期
    まず、地球と火星の会合周期を求めます。ここで、会合とは、中心の惑星を公転する2つの惑星が、中心惑星から見て一直線に並ぶ現象のことです。  
    この時、2つの惑星は接近します。  
    地球の公転周期は$ E=365 $日、火星の公転周期は$ P=687 $日なので、それぞれが1日に進む角度(=角速度)は以下のようになります。
    
    地球が1日に進む角度:  
    #### $$ \frac{360°}{E} $$
    
    火星が1日に進む角度:
    #### $$ \frac{360°}{P} $$

    ここで、  
    #### $$ \frac{360°}{E} > \frac{360°}{P} $$
    の関係があり、地球が火星に追いつく(地球が火星を1周遅れにする)までの期間を会合周期$ S $として導入します。この2つの惑星の角速度の差に会合周期Sをかけることで、火星に対して地球の進んだ角度が1周分、つまり360°となるので、
    #### $$ (\frac{360°}{E}-\frac{360°}{P})×S=360° \qquad \therefore \frac{1}{E}-\frac{1}{P} = \frac{1}{S} $$
    となります。
    以上より、会合周期は、
    #### $$ S=\frac{EP}{P-E}=\frac{365 \times 687}{687-365}=778.7\cdots \fallingdotseq 779日 $$
    となります。779日は約2年2ヶ月なので、地球と火星の会合周期は約2年2ヶ月です。
    '''
    # 2. 軌道平面上の惑星の位置
    '''
    ### 2. 軌道平面上の惑星の位置
    続いて、軌道平面上の惑星の位置を求めます。
    下の図を見てください。
    '''
    image = Image.open('image/惑星軌道円.jpg')
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col2:
        st.image(image, caption="図1 惑星の楕円軌道円と補助円", width=400)
    r'''
    図中に2つの円が見えます。内側の楕円については、ケプラーの第1法則「惑星は楕円軌道をとる」に基づいています。ここで、この楕円軌道の焦点は点Fの太陽です。  
    一方で、外側の円は点Oを中心とした円軌道であり、この補助円を用いることで、計算がしやすくなります。  
    それぞれの変数の概要は以下になります。
    '''
    col1, col2, col3 = st.columns(3)
    with col1:
        r'''
        $ P $: 惑星  
        $ F $: 太陽(焦点)  
        $ a $: 軌道長半径  
        $ f $: 真近点角  
        $ \boldsymbol{ r } = (x, y, 0) $: 動径ベクトル
        '''
    with col2:
        r'''
        $ A $: 近日点  
        $ e $: 軌道離心率  
        $ b $: 軌道短半径  
        $ u $: 離心近点角  
        '''
    r'''
    となります。  
    軌道離心率$e$に関しては、惑星Pに対して焦点$F$と$F'$を用意し、2点の焦点間の関係から導くことが可能です。  
    $F'F$間の長さは三平方の定理より、$2\sqrt{a^{2}-b^{2}}$となり、それは、$2ae$と等しいため、
    ##### $$ e = \frac{\sqrt{a^{2}-b^{2}}}{a} = \sqrt{1-\frac{b^{2}}{a^{2}}} \cdots(1) $$  
    図からわかるように、惑星の座標($x$, $y$)は、  
    ##### $$ x = acosu - ae = rcosf \cdots(2) $$  
    ##### $$ y = bsinu = rsinf \cdots(3) $$  
    となります。三平方の定理より、動径$r$は、  
    ##### $$ r = \sqrt{x^{2}+y^{2}} = \sqrt{a^{2}cos^{2}u-2a^{2}ecosu+a^{2}e^{2}+b^{2}sin^{2}u}  $$
    となります。ここで、(1)式より、
    ##### $$ b^{2} = a^{2}(1-e^{2}) $$
    となるため、
    ##### $$ r = \sqrt{a^{2}cos^{2}u-2a^{2}ecosu+a^{2}e^{2}+a^{2}(1-e^{2})sin^{2}u}  $$
    ##### $$ \quad = a\sqrt{cos^{2}u-2ecosu+e^{2}+sin^{2}u-e^{2}sin^{2}u}$$
    ##### $$ \quad = a\sqrt{1-2ecosu+e^{2}(1-sin^{2}u)}$$
    ##### $$ \quad = a\sqrt{1-2ecosu+e^{2}cos^{2}u}$$
    ##### $$ \quad = a\sqrt{(1-ecosu)^{2}}$$
    ##### $$ \quad = a(1-ecosu)$$
    ##### $$ \therefore r = a(1-ecosu)\cdots(4)$$
    となります。  
    ここで、軌道長半径$ a $や離心率$ e $は定数となるため、変数は離心近点角$ u $のみであり、この値が決まれば軌道平面上の惑星の位置が定まります。
    '''
    # 3. ケプラー方程式
    r'''
    ### 3. ケプラー方程式
    ここからは、ケプラーの第2法則を利用してケプラーの方程式を求めることで、(4)式の離心近点角$ u $の値を定め、惑星の座標を求める方法について考えます。  
    ケプラーの第2法則とは、「単位時間あたりに動径が描く面積が一定」すなわち、焦点である太陽を公転する地球や火星の描く面積が時間に依らず一定であることを言っています。  
    まず、下の図において、$ \Delta t $後にできる扇形$ PHP'' $の面積$ \Delta W $を考えます。
    '''
    image = Image.open('image/楕円軌道.JPG')
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col2:
        st.image(image, caption="図2 楕円軌道", width=600)
    r'''
    図より、位置ベクトル$ \boldsymbol{ r } $と直角の方向に$ \boldsymbol{ v }\Delta t $だけ$ \Delta t $だけ移動したとすると、
    扇形$ PHP'' $を三角形に近似し、面積$ \Delta W $は以下の式で表すことができます。  
    ##### $$ \Delta W = |\frac{\boldsymbol{ r }\times \boldsymbol{ v }\Delta t}{2}| $$
    上式をもとに、惑星の角運動量$ L=r×mv $及び惑星の質量$ m $を用いると、単位時間あたりで惑星が描く面積、すなわち面積速度は、
    #### $$ \frac{ dW }{ dt } = |\frac{\boldsymbol{ r }\times \boldsymbol{ v }}{2}| = \frac{L}{2m} \cdots(5) $$
    となる。ケプラーの第2法則ではこの面積速度が一定となることを示しているため、上の(5)式は一定となります。  
    そこで、定数を$ c $として導入すると、
    #### $$ \frac{ dW }{ dt } = \frac{L}{2m} = c \cdots(6) $$
    と表すことができます。初期時間$ t=t_{0} $の時、惑星の位置はまだ変化がなく、面積$ W=0 $とし、式(6)を$ t $について積分します。
    ##### $$ \int dW = c\int_{t_{0}}^{t} dt = c\left[ t \right]_{t_{0}}^{t} $$
    ##### $$ \therefore W = c(t-t_{0}) $$ 
    惑星が1周すると、$ t-t_{0} $は公転周期$ T $と等しくなります。この時、惑星の描く面積は楕円の面積と等しくなるため、$ W = \pi ab $で
    表されます。(6)式では、時間$ t $あたりの面積変化を定数$ c $で表しています。これについて考えると、公転周期$ T $あたりの面積変化$ W $も
    同様に定数$ c $で表すことができます。すなわち、
    #### $$ c = \frac{ W }{ T } = \frac{\pi ab}{T} $$
    となります。楕円軌道上を運動する惑星の速度は一様ではないため、平均運動$ n $として公転周期$ T $の間に楕円軌道1回転($ 2\pi $)を運動することを考えると、
    #### $$ n = \frac{2\pi}{T} $$
    となり、
    #### $$ c = \frac{\pi ab}{T} = \frac{nab}{2}  $$
    で定数$ c $を表すことができます。よって、(6)式の関係より、
    #### $$ \frac{L}{2m} = c = \frac{nab}{2} $$
    ##### $$ \therefore L = mnab \cdots(7) $$
    となり、(7)式で角運動量を表すことができました。  
    今、角運動量をケプラーの第2法則から求めましたが、$ L=r \times mv $について図1の惑星の楕円軌道円と補助円の関係から、角運動量を表してみます。  
    $ L=r \times mv $について、速度$ v $は、$ v = r\omega $の関係から、半径と角速度の積で求められます。図1において、惑星の描く楕円の半径は
    軌道短半径$ b $であり、角速度は離心近点角$ u $の時間変化$ \frac{du}{dt} $に等しいため、
    #### $$ v = b\frac{du}{dt} $$
    となります。また、$ L=r \times mv $の$ r $については、(4)式を導入すれば良いので、角運動量は、以下のように表されます。
    #### $$ L = mab(1-ecosu)\frac{du}{dt} \cdots(8) $$
    (7)式と(8)式の関係から、
    #### $$ (1-ecosu)\frac{du}{dt} = n $$
    が成り立ちます。初期時間$ t=t_{0} $の時、惑星の位置はまだ変化がなく、離心近点角$ u=0 $とし、上式を$ t $について積分すると、
    ##### $$ \int (1-ecosu)du = n\int_{t_{0}}^{t} dt = n\left[ t \right]_{t_{0}}^{t} $$
    ##### $$ \therefore u-esinu = n(t-t_{0}) \cdots(9) $$ 
    となり、ケプラー方程式として(9)式が求まりました。
    '''
    # 4. 数値計算(オイラー法)によるケプラー方程式の解
    r'''
    ### 4. 数値計算(ニュートン法)によるケプラー方程式の解
    (9)式のケプラー方程式について、数値的に解である離心近点角$ u $を求めます。ここではニュートン法を用いて求めます。  
    ニュートン法とは簡単に言うと、ある関数$ f(x) $について$ f(x) = 0 $となるような解$ x $を求めるアルゴリズムです。  
    (9)式のケプラー方程式について、関数を$ F(u) $を導入し、
    ##### $$ F(u) = u-esinu - n(t-t_{0}) $$ 
    と表します。そして、ニュートン法において、更新前の解を$ u_{n} $、更新後の解を$ u_{n+1} $として、関数$ F(u) $の微分を考えます。  
    すると、
    ##### $$ F'(u) = \frac{\Delta y}{\Delta u} = \frac{F(u)}{u_{n+1}-u_{n}} $$ 
    となるため、更新後の解$ u_{n+1} $は、
    ##### $$ u_{n+1} = u_{n} - \frac{F(u)}{F'(u)} $$ 
    で求められます。そして、上式について複数回更新を繰り返すことによって、解$ u_{answer} $を数値的に求めることができます。  
    最後に、ここで求められた解$ u_{answer} $を(2), (3)式へ代入することで、惑星の軌道平面上の位置$ (x, y, 0) $が決まります。
    ##### $$ x = acosu_{answer} - ae $$  
    ##### $$ y = bsinu_{answer} $$  
    '''



if page_id == 1:
    simulation_page()

if page_id == 2:
    explanation_page()
    