import numpy as np

# When dealing with an array change value after **2, 1->len(observed)
def rrmse(observed, estimated):
    return (np.sqrt(np.mean((observed-estimated)**2)/1)*1/np.mean(observed))