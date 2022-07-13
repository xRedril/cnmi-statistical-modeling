import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from numpy import asarray

Ob = pd.read_csv(os.path.join('inputs/AMR_Inajaran Old Nasa Site_60nm_Selected Duration.csv'))
Ob = asarray(Ob)
obShape = Ob.shape
NY = obShape[0]
ND = obShape[1]
obArray = []

for i in range(ND):
    obArray.append(sorted(Ob[:,i]))

LQ = pd.read_csv(os.path.join("inputs/Quantile_GEV_Lmoments_Obs.csv"))
LQ = asarray(LQ)
LQ = LQ[:,1:]


N1Q = pd.read_csv(os.path.join("inputs/Quantiles_NCM_OneMom_Scaled.csv"))
N1Q = asarray(N1Q)
N1Q = N1Q[:,1:]

N3Q = pd.read_csv(os.path.join("inputs/Quantiles_NCM_ThreeMom_Scaled.csv"))
N3Q = asarray(N3Q)
N3Q = N3Q[:,1:]

P = []
T1 = []
#Cunnane Formula
for i in range(1,NY+1):
    t_calc = (NY + 0.2)/(i - 0.4)
    P_calc = 1/t_calc
    P.append(P_calc)
    T1.append(t_calc)

T1 = sorted(T1)
print(T1)
DT = 4
print(sorted(Ob[:,DT]))
z = np.concatenate((Ob[:,DT], LQ[:,DT], N1Q[:,DT], N3Q[:,DT]))

MAX_V = max(z)
MIN_V = min(z)

ylim = [MAX_V,MIN_V]

#Plotting
plt.figure()
plt.scatter(T1,sorted(Ob[:,DT]), color="none", edgecolor="#000000")
plt.plot(T1, N1Q[:,DT], color="#FF0000", linestyle="dashed")
plt.plot(T1, N3Q[:,DT], color="#2B547E", linestyle="dashed")
plt.show()
