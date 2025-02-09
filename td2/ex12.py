import math
from scipy.optimize import fixed_point
import matplotlib.pyplot as plt

K = 10 # max number of attemps before dropping
m = 6 # number of collisions until contention window becomes constant
sigma = 50 * (10**-6) # slot duration
L = 8584 # number of bits in a packet
ACK = 240 # number of bits in ACK
SIFS = 28 * (10**-6) # duration of SIFS
DIFS = 128 * (10**-6) # duration of DIFS
CW_min = 32 # b_0
C = 10**6 # physical data rate

Tc = DIFS
Ts = L/C + ACK/C + DIFS

n = 1

def func_Gamma(beta):
    return 1 - math.pow(1-beta, n-1)
def func_G(gamma):
    numerator_G = 0
    denominator_G = 0
    for i in range(0, K+1):
        numerator_G += math.pow(gamma, i)
        denominator_G += math.pow(gamma, i)*i
    return numerator_G/denominator_G
def func_composite(gamma):
    return func_Gamma(func_G(gamma))

S = []
S_over_C = []

for i in range(2, 30):
    n = i
    gamma = fixed_point(func_composite, 0.5)
    beta = func_G(gamma)

    EVal_R = (n*beta*math.pow(1 - beta, n-1)*L)/(1 - math.pow(1 - beta, n))
    prob_aux =  math.pow(1-beta,n-1)
    EVal_X = (sigma/(1 - math.pow(1-beta,n))) + Ts*prob_aux + Tc*(1-prob_aux)

    S.append(EVal_R/EVal_X)
    S_over_C.append(EVal_R/(C*EVal_X))

# Plot S/C as a function of n
plt.plot(range(2, 30), S_over_C, marker='o')
plt.xlabel('Number of Stations (n)')
plt.ylabel('Normalized Throughput (S/C)')
plt.title('Normalized Saturated Throughput vs Number of Stations')
plt.grid(True)
plt.show()