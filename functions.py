from calendar import month
import numpy as np


# 楕円軌道関数 Ellipse
def calc_coordinates(i, a, e):
    u = np.pi/180*i # 等速で変化する離心近点角
    b=a*np.sqrt(1-np.power(e,2)) # 軌道短半径 b=a√(1-e^2)
    x=a*np.cos(u)-a*e # x座標 acosu-ae
    y=b*np.sin(u) # y座標 bsinu
    return x, y

# 楕円軌道の関数
def ellipse_Kepller(u, a, e):
    b=a*np.sqrt(1-np.power(e,2))
    x=a*np.cos(u)-a*e
    y=b*np.sin(u)
    return x, y

# [ユリウス日の計算](https://jcometobs.web.fc2.com/astrocalc/time/julian_cal.html) CalcDate
def DayToJD(year, month, day, hour, minute):
    # 世界標準時UTの計算
    UT_day = day+(hour-9+minute/60)/24
    # 月が3月未満(1月、2月)
    if month < 3:
        jd_month = month + 12
        jd_year = year - 1
    else:
        jd_month = month
        jd_year = year
    aa = int(jd_year/100)
    bb = 2.0 - aa + int(aa/4.0)
    JD = int(365.25*jd_year) + int(30.6001*(jd_month + 1)) + UT_day + bb + 1720994.5
    print('JD:', JD)
    return JD

def JDToDay(JD):
    # JDはUTを変換したものなので，UT+9hのため9/24を加える
    UT_JD = JD + 0.5 + 9/24
    JDi = int(UT_JD)
    JDf = UT_JD - JDi
    if JDi > 2299160.0:
        aa = int((JDi - 1867216.25) / 36524.25)
        JDi = JDi + (1.0 + aa - int(aa / 4.0))
    
    bb = JDi + 1524.0
    YY = int((bb - 122.1) / 365.25)
    DD = bb - int(YY * 365.25)
    MM = int(DD / 30.6001)
    DDay= DD - int(MM * 30.6001) + JDf
    Day = int(DDay)
    HH = DDay - Day
    Hour = int(HH*24)
    Minute = round((HH*24 - Hour)*60)
    if MM < 14:
        Month = MM - 1
    else:
        Month = MM - 13
    if Month > 2:
        Year = YY - 4716
    else:
        Year = YY - 4715
    return Year, Month, Day, Hour, Minute

def Kepller_function(mean_moment, t, t0, e, u):
    return u - e*np.sin(u) - mean_moment*(t - t0)

def diff_function(e, u):
    return 1 - e*np.cos(u)

# 座標変換
def coordinate_transformation(xx,yy,cosohm,sinohm,cosi,sini,cosomega,sinomega):
    Xc=xx*(cosohm*cosomega-sinohm*cosi*sinomega)-yy*(cosohm*sinomega+sinohm*cosi*cosomega)
    Yc=xx*(sinohm*cosomega+cosohm*cosi*sinomega)-yy*(sinohm*sinomega-cosohm*cosi*cosomega)
    Zc=xx*sini*sinomega+yy*sini*cosomega
    return Xc,Yc,Zc