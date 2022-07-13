import os
import numpy as py
import pandas as pd
import matplotlib.pyplot as plt 
from numpy import asarray
import csv

#Importing data
Ob = pd.read_csv(os.path.join('inputs/AMR_Inajaran Old Nasa Site_60nm_Selected Duration.csv'))
Ob = asarray(Ob)

LQ = pd.read_csv(os.path.join('inputs/Quantile_GEV_Lmoments_Obs.csv'))
LQ = asarray(LQ)
LQ = LQ[:,1:]

NQ = pd.read_csv(os.path.join('inputs/Quantile_GEV_NCMs_Obs.csv'))
NQ = asarray(NQ)
NQ = NQ[:,1:]

#Getting the number of rows and columns for Ob
nShape = Ob.shape
nRow = nShape[0]
nCol = nShape[1]
P = []

#Cunnane Formula
for i in range(0,nRow):
    t_calc = (nRow + 0.2)/(i - 0.4)
    P_calc = 1/t_calc
    P.append(P_calc)

X = py.sort(Ob[ :,0])

#Plotting
plt.figure()
plt.scatter(P,X, color="none", edgecolor="#000000")
plt.plot(P, LQ[:,0], color="#2B547E", linestyle="dashed")
plt.plot(P, NQ[:,0], color="#FF0000")
plt.show()

#RMSE function
def RMSE(observed, estimated):
    return py.sqrt(py.mean(py.square(observed - estimated)))

#RMSE for L-Moments
RMSE_L_Unsorted = []
for i in range(nCol):
    Temp = RMSE(Ob[:,i],LQ[:,i])
    RMSE_L_Unsorted.append(Temp)

print(RMSE(Ob[0],LQ[0]))

RMSE_L = py.sort(RMSE_L_Unsorted)

#RMSE for NCMs
RMSE_N_Unsorted = []
for i in range(nCol):
    Temp = RMSE(Ob[:,i],NQ[:,i])
    RMSE_N_Unsorted.append(Temp)

RMSE_N = py.sort(RMSE_N_Unsorted)

#Combining both RMSEs
numberCol = []
for i in range(1,nCol + 1):
    numberCol.append(i)
print(numberCol)
RMSE = list(zip(numberCol,RMSE_L,RMSE_N))

#Output File of RMSEs
header = ['','RMSE_L', 'RMSE_N']

with open('output/Compare_RMSEs_Test.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(RMSE)

print("Output File Success")