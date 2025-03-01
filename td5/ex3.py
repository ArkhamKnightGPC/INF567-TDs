import math
from scipy import special

N0 = -174
W = 125 * (10**3)

N = N0 + 10*math.log10(W)
print(f"N = {N}")

SNR = -20
Pmin = N + SNR

totalGain = 6 + 10*math.log(2)
print(f"sum of gain of the two antennas = {totalGain}dB")
totalLoss = 3 + 18

def Q(x):
    return 0.5*special.erfc(x/math.sqrt(2))
def Q_inv(x):
    aux = math.sqrt(2)*special.erfcinv(2*x)
    assert(math.pow(Q(aux) - x, 2) < 0.1)
    return aux

Pout = 0.9
Ptx = 16.15
shadowingMargin = Pmin - Ptx - totalGain + totalLoss
shadowingDeviation = (shadowingMargin)/Q_inv(1 - Pout)
print(f"shadowing margin = {shadowingMargin}")
print(f"shadowing std = {shadowingDeviation}")

MAPL = Ptx + totalGain - totalLoss - Pmin
print(f"MAPL = {MAPL}db")

fc = 868 * (10**6)
hb = 30
A_urban = 69.55 + 26.16*math.log10(fc) - 13.82*math.log10(hb)
B_urban = 44.9 - 6.55*math.log10(hb)
C_urban = 3.2*math.pow(math.log10(11.75*fc), 2) - 4.97
print(f"A_urban = {A_urban}")
print(f"B_urban = {B_urban}")
print(f"C_urban = {C_urban}")
d_urban = math.pow(10, (MAPL - A_urban + C_urban)/B_urban)
print(f"d_urban = {d_urban}m")

A_rural = A_urban
B_rural = B_urban
C_rural = 4.78*math.pow(math.log10(fc), 2) - 18.33*math.log10(fc) + 40.94
print(f"A_rural = {A_rural}")
print(f"B_rural = {B_rural}")
print(f"C_rural = {C_rural}")
d_rural = math.pow(10, (MAPL - A_rural + C_rural)/B_rural)
print(f"d_rural = {d_rural}m")
