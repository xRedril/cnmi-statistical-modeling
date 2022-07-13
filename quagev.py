import numpy.lib.scimath as sm
from numpy import exp as xp

#There is no library that I could find that contains quagev function so I recreated it here.
def quagev(F, para):
    U = para[0]
    A = para[1]
    G = para[2]
    if A <= 0:
        print("Parameters Invalid")
        return
    if F <= 0 or F >= 1:
        if F == 0 and G < 0:
            QUAGEV = U + A / G
        elif F == 1 and G > 0:
            QUAGEV = U + A / G
        else:
            print("F Value Invalid")
            return

        print("F Value Invalid")
        return
    else:
        Y = -sm.log(-sm.log(F))
        if G != 0:
            Y = (1 - xp(-G * Y)) / G
        QUAGEV = U + A * Y
        return (QUAGEV)