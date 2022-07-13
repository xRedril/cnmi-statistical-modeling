import pandas as pd
import numpy as np
import quagev as qg
from numpy import asarray

BP = 3

# Import data
ScaleExS = pd.read_csv("inputs/Scaling Exponents_Short.csv")
ScaleExL = pd.read_csv("inputs/Scaling Exponents_Long.csv")
ParGev = pd.read_csv("inputs/ParamGEV_NCM_Obs.csv")

betaS = ScaleExS.iloc[0, 1]
betaL = ScaleExL.iloc[0, 1]

TShi = ParGev.iloc[0, ParGev.shape[1]-1]
TAlpha = ParGev.iloc[1, ParGev.shape[1]-1]
TKappa = ParGev.iloc[2, ParGev.shape[1]-1]

# Duration
Dur = [15, 30, 45, 60, 120, 180, 360, 720, 1440]

# One-Moment Scaling method
ND = len(Dur)-1

tShi = []
tAlpha = []
tKappa = []

for i in range(0, ND+1):
    tKappa.append(TKappa)

# Long Period
for i in range(BP, ND):
    T = Dur[ND]
    t = Dur[i]
    tAlphaCalc = np.exp(betaL * (np.log(t) - np.log(T)) + np.log(TAlpha))
    tAlpha.append(tAlphaCalc)
    tShiCalc = np.exp(betaL * (np.log(t) - np.log(T)) + np.log(TShi))
    tShi.append(tShiCalc)

tAlpha.append(TAlpha)
tShi.append(TShi)

# Short Period
for i in range(0, BP):
    T = Dur[BP]
    t = Dur[i]
    tAlphaCalc = np.exp(betaS * (np.log(t) - np.log(T)) + np.log(tAlpha[i]))
    tAlpha.insert(0, tAlphaCalc)
    tShiCalc = np.exp(betaS * (np.log(t) - np.log(T)) + np.log(tShi[i]))
    tShi.insert(0, tShiCalc)

tAlpha.sort()
tShi.sort()

# Save Scaled-GEV Parameters
npArray = [tShi, tAlpha, tKappa]
df = pd.DataFrame(data=npArray, columns=["D_15min", "D_30min", "D_45min", "D_1h", "D_2h", "D_3h", "D_6h", "D_12h", "D_24h"])
df.index = ['tShi'] + ['tAlpha'] + ['tKappa']
df.to_csv("output/ParamGEV_Scaled_NCM_OneMom.csv")

# Estimate Quantiles and Save Quantiles

# Plotting position
# Cunnane Formula: T=(N+0.2)/(m-0.4)
ScaledParmGEV = asarray([tShi, tAlpha, tKappa])
N = 40
P = []
for i in range(1, N+1):
    tCalc = (N+0.2) / (i-0.4)
    pCalc = 1 / tCalc
    P.append(pCalc)

# Estimating Quantiles
# Using imported quagev.py method
Q = np.zeros(shape=(N, ND+1))
for i in range(ND+1):
    for j in range(N):
        Q[j, i] = (qg.quagev(P[j], ScaledParmGEV[:,i]))

quantileFrame = pd.DataFrame(data=Q, columns=["D_15min", "D_30min", "D_45min", "D_1h", "D_2h", "D_3h", "D_6h", "D_12h", "D_24h"])

# Save the estimated quantiles
quantileFrame.to_csv("output/Quantiles_NCM_OneMom_Scaled.csv")