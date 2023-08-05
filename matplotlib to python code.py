import numpy as np
import matplotlib.pyplot as plt

# Constant Declaration
K = 1.38065e-23  # Boltzman Constant
q = 1.602e-19  # Electron's Charge
Iscn = 13.84  # Desigerable Short Circuit Current
Vocn = 48.92  # Desigerable Open Circuit Voltage
Kv = -0.123  # Temperature Voltage Constant
Ki = 0.0032  # Temperature Current Constant
Ns = 54  # Number of Series Connected Cells
T = 25 + 273  # Operating Temperature in Kelvin
Tn = 30 + 273  # Temperature at STC
Gn = 1500  # Irradiance at STC
a = 2.0  # Diode Ideality Constant [1 < a < 2]
Eg = 1.2  # Band Gap of silicon at Temperature of STC condition [25 deg. Cel]
G = 800  # Actual Irradiance
Rs = 0.221  # Series Resistance of Equivalent PV cell
Rp = 415.405  # Parallel Resistance of Equivalent PV cell

# Parameter's Value Calculation
Vtn = Ns * ((K * Tn) / q)  # Equation 2
I0n = Iscn / ((np.exp(Vocn / (a * Vtn))) - 1)  # Equation 5
I0 = I0n * ((Tn / T) ** 3) * np.exp(((q * Eg / (a * K)) * ((1 / Tn) - (1 / T))))  # Equation 4
Ipvn = Iscn
Ipv = (G / Gn) * (Ipvn + Ki * (T - Tn))  # Equation 3
Vt = Ns * ((K * T) / q)

Voc_range = np.arange(Vocn, 0, -0.1)
I = np.zeros(len(Voc_range))
Pi = np.zeros(len(Voc_range))
Vi = np.zeros(len(Voc_range))

for i, V in enumerate(Voc_range[:-1]):  # Adjusted loop range to avoid the last element
    I_term1 = I0 * (np.exp((V + I[i] * Rs) / (Vt * a)) - 1)  # Part of Equation 1
    I_term2 = (V + I[i] * Rs) / Rp  # Part of Equation 1
    I[i + 1] = Ipv - (I_term1 + I_term2)  # Equation 1

    if I[i] > 0:  # Negative Power and Current Control Loop
        I[i] = I[i]
    else:
        I[i] = 0

    Pi[i] = V * I[i]
    Vi[i] = V

# Graphical Interface
plt.figure(1)
plt.plot(Vi[:i], I[:i], 'r', linewidth=2.5)
plt.xlabel('Voltage (volt)')
plt.ylabel('Current (Amp)')

plt.figure(2)
plt.plot(Vi[:i], Pi[:i], 'k', linewidth=2.5)
plt.xlabel('Voltage (volt)')
plt.ylabel('Power (Watt)')

plt.show()

# Calculate Maximum Power Point (MPP)
ffg = np.argmax(Pi)
FF = (I[ffg] * Vi[ffg]) / (Iscn * Vocn)  # Corrected Fill Factor calculation
print('Open Circuit Voltage = %3.5f' % Vocn)
print('Short Circuit Current = %3.5f' % Iscn)
print('PMAX = %3.5f' % max(Pi))
print('VMAXP = %3.5f' % Vi[ffg])
print('IMAXP = %3.5f' % I[ffg])
print('FF = %3.5f' % FF)
