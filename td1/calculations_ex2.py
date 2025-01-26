import math
from scipy import special

carrier_frequency = 2.6*(10**9)
c = 3*(10**8)
wavelength = c/carrier_frequency

signal_bandwidth = 20*(10**6)
reference_distance = 1
path_loss_exponent = 3.5

shadowing_standard_deviation_dB = 8
shadowing_standard_deviation = math.pow(10, shadowing_standard_deviation_dB/10)

transmitter_power_dBm = 46
transmitter_power = math.pow(10, transmitter_power_dBm/10)

antenna_gain_dBi = 19
antenna_gain = math.pow(10, antenna_gain_dBi/10)

physical_data_rate = 10*(10**6) #bits per second
success_rate = 0.99

# Question 6
K = math.pow((wavelength*math.sqrt(antenna_gain))/(4*math.pi*reference_distance), 2)
K_db = 10*math.log10(K)
print(f"K = {K}     K[dB] = {K_db}dB")

SNR_min = math.pow(2, physical_data_rate/signal_bandwidth) - 1
SNR_min_dB = 10*math.log10(SNR_min)
print(f"SNR_min = {SNR_min}  SNR_min_dB = {SNR_min_dB}")

N_0_dBm = -174
N_0 = math.pow(10, N_0_dBm/10)
print(f"N_0 = {N_0_dBm}dBm or {N_0}")
received_power_edge_mW = SNR_min*N_0*signal_bandwidth
received_power_edge_dBm = 10*math.log10(received_power_edge_mW)
print(f"P_r,edge = {received_power_edge_mW}mW or {received_power_edge_dBm}dBm")

def Q(x):
    return 0.5*special.erfc(x/math.sqrt(2))
def Q_inv(x):
    aux = math.sqrt(2)*special.erfcinv(2*x)
    assert(math.pow(Q(aux) - x, 2) < 0.1)
    return aux
aux = (received_power_edge_dBm - transmitter_power_dBm - K_db - shadowing_standard_deviation_dB*Q_inv(success_rate))/(10*path_loss_exponent)
d_edge = reference_distance*math.pow(10, -aux)
print(f"d_edge = {d_edge}")

#Question 8
Pr_min_dBm = -110

P_R = transmitter_power_dBm + K_db + 10*path_loss_exponent*math.log10(reference_distance/d_edge)

a = (Pr_min_dBm - P_R)/shadowing_standard_deviation_dB
b = 10*path_loss_exponent*math.log10(math.e)/shadowing_standard_deviation_dB
print(f"a={a} b={b}")
p_covered = Q(a) + math.exp((2 - 2*a*b)/(b*b))*Q(2/b - a)
print(f"p_covered = {p_covered}")
