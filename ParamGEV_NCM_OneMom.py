import os
import numpy as np
import pandas as pd
from numpy import asarray
import csv
import quagev as qg

# import data
ScaleExS = pd.read_csv(os.path.join('inputs/Scaling Exponents_Short.csv'))
ScaleExS = asarray(ScaleExS)
betaS = ScaleExS[0][1]

ScaleExL = pd.read_csv(os.path.join('inputs/Scaling Exponents_Long.csv'))
ScaleExL = asarray(ScaleExL)
betaL = ScaleExL[0][1]

ParGev = pd.read_csv(os.path.join('inputs/ParamGEV_NCM_Obs.csv'))
ParGev = asarray(ParGev)

ParGevShape = ParGev.shape
nRow = ParGevShape[0]
nCol = ParGevShape[1]

TShi = ParGev[0][nCol-1]
TAlpha = ParGev[1][nCol-1]
TKappa = ParGev[2][nCol-1]

# Duration
Dur = [5, 10, 15, 30, 60, 120, 360, 720, 1440]

# ================================================
# One-Moment Scaling method ----
# ================================================
    # Alpha(t) = lamda^beta * Alpha(T)
    # Alpha(t) = beta*log(t/T) + log(Alpha(T))
    # Alpha(t) = beta*{log(t) - log(T)} + log(Alpha(T))

BP = 4
ND = len(Dur) - 1

tShi = [0] * ND
tAlpha = [0] * ND
tKappa = [0] * ND

tShi.append(TShi)
tAlpha.append(TAlpha)
tKappa.append(TKappa)

# Replacing zeros with value of Tkappa
tKappa = [TKappa if x==0 else x for x in tKappa]

# Temporary Arrays to store long and short version of shi and alpha
longTAlpha = []
longTShi = []
shortTShi = []
shortTAlpha = []

#Long Period
for i in range(0,ND+1):
    T = Dur[ND]
    t = Dur[i]
    longTAlpha.append(np.exp(betaL * (np.log(t) - np.log(T)) + np.log(TAlpha)))
    longTShi.append(np.exp(betaL * (np.log(t) - np.log(T)) + np.log(TShi)))

# Short Period
for i in range(0,BP):
    T = Dur[BP-1]
    t = Dur[i]
    tAlphaCalc = np.exp(betaS * (np.log(t) - np.log(T)) + np.log(longTAlpha[BP-1]))
    tShiCalc = np.exp(betaS * (np.log(t) - np.log(T)) + np.log(longTShi[BP-1]))
    shortTAlpha.append(tAlphaCalc)
    shortTShi.append(tShiCalc)

# Removing indexes 0 to BP for Long Period
for i in range(0,BP):
    longTShi.pop(0)
    longTAlpha.pop(0)

# Merging the short period and long period.
tShi = shortTShi + longTShi
tAlpha = shortTAlpha + longTAlpha

namesCol = ["D_15min","D_30min", "D_45min", "D_1h", "D_2h","D_3h", "D_6h", "D_12h", "D_24h"]

#print(scaledParmGEV)

#Save the estimated quantiles
with open('output/ParamGEV_NCM_OneMom_Scaled.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    #write the header
    writer.writerow(namesCol)

    # write multiple rows
    writer.writerow(tShi)
    writer.writerow(tAlpha)
    writer.writerow(tKappa)

ScaledParmGEV = asarray([tShi,tAlpha,tKappa])

#Estimate quantiles and save quantiles
P = []
N = 30
#Cunnane Formula
for i in range(1, N+2):
    t_calc = (N + 0.2)/(i - 0.4)
    P_calc = 1/t_calc
    P.append(P_calc)

P = sorted(P)

#Estimating Quantiles
Q = np.zeros(shape = (N, ND+1))
for i in range(ND+1):
    for j in range(N):
        Q[j, i] = (qg.quagev(P[j], list(ScaledParmGEV[:,i])))


#Save the estimated quantiles
with open('output/Quantiles_NCM_OneMom_Scaled.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    #write the header
    writer.writerow(namesCol)

    # write multiple rows
    writer.writerows(Q)