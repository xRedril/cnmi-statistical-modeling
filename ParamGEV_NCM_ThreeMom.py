import pandas as pd
import numpy as np

from R_Code_Conversion import paramGev
from scipy.stats import genextreme

BP = 4

x = pd.read_csv("inputs/AMR_Inajaran Old Nasa Site_60nm_Selected Duration.csv")

NDur = x.shape[1]
NYear = x.shape[0]
print(x)
ScaleExS = pd.read_csv("inputs/Scaling Exponents_Short.csv")
ScaleExL = pd.read_csv("inputs/Scaling Exponents_Long.csv")

betaS = ScaleExS['x']
betaL = ScaleExL['x']

Dur = [15, 30, 45, 60, 120, 180, 360, 720, 1440]

T1 = Dur[len(Dur) - 1]
T2 = Dur[BP - 1]
T1N = NDur
T2N = BP

x = x.sort_values('1440min', ascending=True)
Temp = x['1440min']
Temp = Temp.reset_index(drop=True)
Temp2 = Temp**2
Temp3 = Temp**3


Tempmean = Temp.mean()
Temp2mean = Temp2.mean()
Temp3mean = Temp3.mean()

# Long Period
ncm1 = []
ncm2 = []
ncm3 = []

for i in range(BP-1, NDur):
    t = Dur[i]
    ncm1Calc = np.exp(betaL[0] * (np.log(t) - np.log(T1)) + np.log(Tempmean))
    ncm1.append(ncm1Calc)
    ncm2Calc = np.exp(betaL[1] * (np.log(t) - np.log(T1)) + np.log(Temp2mean))
    ncm2.append(ncm2Calc)
    ncm3Calc = np.exp(betaL[2] * (np.log(t) - np.log(T1)) + np.log(Temp3mean))
    ncm3.append(ncm3Calc)

# Short Period
ncm1short = []
ncm2short = []
ncm3short = []

for i in range(0, BP-1):
    t = Dur[i]
    ncm1shortCalc = np.exp(betaS[0] * (np.log(t) - np.log(T2)) + np.log(ncm1[T2N - 4]))
    ncm1short.append(ncm1shortCalc)
    ncm2shortCalc = np.exp(betaS[1] * (np.log(t) - np.log(T2)) + np.log(ncm2[T2N - 4]))
    ncm2short.append(ncm2shortCalc)
    ncm3shortCalc = np.exp(betaS[2] * (np.log(t) - np.log(T2)) + np.log(ncm3[T2N - 4]))
    ncm3short.append(ncm3shortCalc)

ncm1 = ncm1short + ncm1
ncm2 = ncm2short + ncm2
ncm3 = ncm3short + ncm3

print(ncm1)
print(ncm2)
print(ncm3)
# Estimate parameters using the three moments method. [Need to create paramGev method]

Param = []



