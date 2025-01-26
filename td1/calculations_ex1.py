import math
import numpy as np 
import matplotlib.pyplot as plt

transmitter_power_dBm = 46
transmitter_power_mW = math.pow(10, transmitter_power_dBm/10)
print(f"pt = {transmitter_power_mW}mW")

transmitter_gain_dBi = 16
transmitter_gain = math.pow(10, transmitter_gain_dBi/10)

receiver_gain_dBi = 0
receiver_gain = math.pow(10, receiver_gain_dBi/10)

print(f"gt = {transmitter_gain}  gr = {receiver_gain}")

distances = [50, 100, 250, 500, 1000]
received_power_dBm = [1.2, -10.4, -19.8, -30.4, -50.4]

received_power_mW = [math.pow(10, pr_dBm/10) for pr_dBm in received_power_dBm]

print(f"pr = {received_power_mW}")

#Question 1
c = 3*(10**8)
carrier_frequency = 900*(10**6)
wavelength = c/carrier_frequency
d0 = 1

K = ((wavelength*math.sqrt(transmitter_gain*receiver_gain))/(4*math.pi*d0))**2
K_dB = 10*math.log10(K)
print(f"K = {K}  K[dB] = {K_dB}")

#Question 2

# the MSE is an order 2 polynomial A alpha^2 + B alpha + C, let's compute the coefficients
A = 0
B = 0
C = 0
#transmitter_power_dB = 10*math.log(transmitter_power_mW*(10**(-3)))
#received_power_dB = [10*math.log(power_mW*(10**(-3))) for power_mW in received_power_mW]
for i in range(5):
    aux = 10*math.log10(K*transmitter_power_mW) - received_power_dBm[i]
    aux2 = 10*math.log10(d0/distances[i])
    B += 2*aux2*aux
    A += aux2**2
    C += aux**2
A /= 5
B /= 5
C /= 5

#Now let's plot the MSE as function of alpha 
alpha_vals = np.linspace(-10, 10, 400)
MSE = A*(alpha_vals**2) + B*alpha_vals + C 
plt.plot(alpha_vals, MSE, label=f'{A}x^2 + {B}x + {C}')
plt.xlabel('alpha')
plt.ylabel('MSE')
plt.title('Finding optimal alpha')
plt.legend()
plt.grid(True)
plt.savefig('alpha_plot.png')

opt_alpha = -B/(2*A)
print(f"opt_alpha = {opt_alpha}")

#now we can predict received power at 750m
pr_750 = transmitter_power_mW*K*math.pow(d0/750, opt_alpha)
pr_750_dBm = 10*math.log10(pr_750)
print(f"pr(750m) = {pr_750}  or in dBm {pr_750_dBm}")

#Question 3
variance = 0
def simplified_model(d):
    return 10*math.log10(transmitter_power_mW*K*math.pow(d0/d, opt_alpha))
    #return transmitter_power_mW*K*((d0/d)**opt_alpha)
for i in range(5):
    variance += ((received_power_dBm[i] - simplified_model(distances[i]))**2)/5

sigma_shadowing = math.sqrt(variance)
sigma_shadowing_dB = 10*math.log10(sigma_shadowing)
print(f"variance = {variance}  sigma shadowin = {sigma_shadowing} or {sigma_shadowing_dB}dB")

#Question 4
carrier_frequency = 30*(10**9)
alpha = 2.5
transmitter_gain_dBi = 30
receiver_gain_dBi = 5

wavelength = c/carrier_frequency
transmitter_gain = math.pow(10, transmitter_gain_dBi/10)
receiver_gain = math.pow(10, receiver_gain_dBi/10)

K = ((wavelength*math.sqrt(transmitter_gain*receiver_gain))/(4*math.pi*d0))**2
K_dB = 10*math.log10(K)
print(f"new K = {K}  new K[dB] = {K_dB}")

log10_N = (pr_750_dBm - 10*math.log10(K*transmitter_power_mW*math.pow(d0/750, alpha)))/10
N = math.pow(10, log10_N)
print(f"N = {N}")

#Question 5
N_d = math.pow(10, 16/10)
print(f"N_d = {N_d}")

N_d = round(N_d) #we need an integer number of antennas
freq1 = 900*(10**6)
freq2 = 30*(10**9)
dipole_size1 = c/(2*freq1)
dipole_size2 = c/(2*freq2)

size_two_columns = (N_d/2)*dipole_size1
print(f"two columns => {size_two_columns}")
size_square_panel = math.sqrt(N_d)*dipole_size2
print(f"square panel => {size_square_panel}")