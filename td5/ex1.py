import math

Isleep = 0.1 * (10**-6) #amps
Itx = 125 * (10**-3) #amps
Irx = 10 * (10**-3) #amps
C = 2500 * (10**-3)#Ah (battery capacity)
B = 125 * (10**3) #Hz
SF = 12
preamble = 12 #symbols
payload = 51*8 #bits
code_rate = 4/5
phy_mac_overhead = 324 #bits
Ttransmission = 2*60*60 #seconds (transmission period)


N = math.pow(2, SF)
print(f"N = {N}")
Tsymbol = N/B
print(f"Tsymbol = {Tsymbol} seconds")

print("--- In class A ---")
n = preamble + (1/SF)*(payload/code_rate + phy_mac_overhead)
print(f"n = {n} symbols")
Ttx = round(n)*Tsymbol #packet transmission time
print(f"Ttx = {Ttx} seconds")
Twindow = preamble*Tsymbol 
print(f"Twindow = {Twindow} seconds")
delta = 1
Trx = 2*(delta + Twindow) #packet receive time
print(f"Trx = {Trx} seconds")
Tsleep = Ttransmission - Ttx - Trx
I = (Itx*Ttx + Irx*Trx + Isleep*Tsleep)/Ttransmission
print(f"Iavg = {I} A")
BatteryLife = C/I #hours
print(f"L = {BatteryLife} hours = {BatteryLife/(24*365.25)} years")
print("----------")

print("--- In class B ---")
SFbeacon = 9
Nbeacon = math.pow(2, SFbeacon)
bandwidthBeacon = 125 * (10**3)
symbolDurationBeacon = Nbeacon/bandwidthBeacon
print(f"beacon symbol duration = {symbolDurationBeacon}s")

codingRateBeacon = 4/5
symbolsInPayload = 17*8/(codingRateBeacon*SFbeacon)
print(f"number of symbols in payload = {symbolsInPayload}")

beaconDuration = symbolDurationBeacon*29
print(f"beacon duration = {beaconDuration}")

SFping = 12
Nping = math.pow(2, SFping)
bandwidthPing = bandwidthBeacon
symbolDurationPing = Nping/bandwidthPing
print(f"ping slot symbol duration = {symbolDurationPing}s")
pingDuration = 12*symbolDurationPing
print(f"ping duration = {pingDuration}s")

pingPeriodicity = 1
beaconPeriodicity = 128
Trx_B = (beaconDuration/beaconPeriodicity + pingDuration/pingPeriodicity)/(1/beaconPeriodicity + 1/pingPeriodicity)
print(f"Trx_B = {Trx_B}s")

I_B = (Itx*Ttx + Irx*Trx_B + Isleep*Tsleep)/Ttransmission
print(f"Iavg_B = {I_B} A")
BatteryLife_B = C/I_B #hours
print(f"L = {BatteryLife_B} hours = {BatteryLife_B/(24*365.25)} years")
print("----------")

print("--- In class B ---")
Trx_C = Trx/2
print(f"Trx_C = {Trx_C}s")

I_C = (Itx*Ttx + Irx*Trx_C + Isleep*Tsleep)/Ttransmission
print(f"Iavg_C = {I_C} A")
BatteryLife_C = C/I_C #hours
print(f"L = {BatteryLife_C} hours = {BatteryLife_C/(24*365.25)} years")
print("----------")
print("----------")