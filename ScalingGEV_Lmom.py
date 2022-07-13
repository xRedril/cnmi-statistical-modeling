import pandas as pd
import numpy as np

BP = 3

x = pd.read_csv("AMR_Inajaran Old Nasa Site_60nm_Selected Duration.csv")

NDur = x.shape[1]
NYear = x.shape[0]

x = pd.DataFrame(np.sort(x.values, axis=0), index=x.index, columns=x.columns)

ScaleExS = pd.read_csv("Scaling Exponents_Short.csv")
ScaleExL = pd.read_csv("Scaling Exponents_Long.csv")

betaS = ScaleExS['x']
betaL = ScaleExL['x']

Dur = [15, 30, 45, 60, 120, 180, 360, 720, 1440]

# Estimate Quantiles using Simple Scaling Properties
T1 = Dur[len(Dur) - 1]
T2 = Dur[BP]
T1N = Dur
T2N = BP

x1440 = x["1440min"]
print(x1440)

# Long Period
QualLm = pd.DataFrame()
print(QualLm)
for i in range(0, NDur-1):
    t = Dur[i]
    qualLmCalc = np.exp(betaL[0] * (np.log(t)-np.log(T1)) + np.log(x1440[i]))
    QualLm.append(qualLmCalc)
# Short Period
