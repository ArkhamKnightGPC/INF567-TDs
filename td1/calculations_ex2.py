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

boltzmann_cte = 1.38*(10**-23)
temperature = 300
N_0_dBm = 10*math.log10(boltzmann_cte*temperature)
N_0 = math.pow(10, N_0_dBm/10)
print(f"N_0 = {N_0_dBm}dBm or {N_0}")
received_power_edge_mW = SNR_min*N_0*signal_bandwidth
received_power_edge_dBm = 10*math.log10(received_power_edge_mW)
print(f"P_r,edge = {received_power_edge_mW}mW or {received_power_edge_dBm}dBm")

aux = (received_power_edge_dBm - transmitter_power_dBm - K_db - shadowing_standard_deviation_dB*special.erfcinv(2*success_rate))/(10*path_loss_exponent)
d_cell = reference_distance*math.pow(10, -aux)
print(f"d_cell = {d_cell}")

#Question 8
def Q(x):
    return 0.5*special.erfc(x/math.sqrt(2))
def Q_inv(x):
    aux = math.sqrt(2)*special.erfcinv(2*x)
    assert(math.pow(Q(aux) - x, 2) < 0.1)
    return aux

Pr_min_dBm = -110

aux = Pr_min_dBm - transmitter_power_dBm
aux2 =  Q_inv(0.9)
new_K_dB = (shadowing_standard_deviation_dB*aux2 - aux)
new_K = math.pow(10, new_K_dB/10)
print(f"K = {new_K_dB}dB or {new_K}")

a = (Pr_min_dBm - new_K_dB - transmitter_power_dBm)/shadowing_standard_deviation
b = (10*path_loss_exponent)/(math.log(10)*shadowing_standard_deviation)
p_covered =Q(a) + math.exp((2 - 2*a*b)/(b*b))*Q(2/b - a)
print(f"p_covered = {p_covered}")